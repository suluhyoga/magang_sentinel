import sys, os, torch, shutil
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import numpy as np
import pandas as pd
from datasets import Dataset
from transformers import (
    AutoTokenizer, AutoModelForSequenceClassification, 
    Trainer, TrainingArguments, DataCollatorWithPadding, EarlyStoppingCallback
)
from sklearn.model_selection import train_test_split
from sklearn.utils.class_weight import compute_class_weight
from sklearn.metrics import accuracy_score, f1_score
from core.text_preprocessing import preprocess_text

BASE_MODEL = "indobenchmark/indobert-base-p1"
DATA_PATH = "dataset/report_classifier.csv"
MODEL_DIR = "model/emergency_classifier"

def compute_metrics(eval_pred):
    logits, labels = eval_pred
    preds = np.argmax(logits, axis=1)
    return {"accuracy": accuracy_score(labels, preds), "f1": f1_score(labels, preds)}

class WeightedTrainer(Trainer):
    def compute_loss(self, model, inputs, return_outputs=False, num_items_in_batch=None, **kwargs):
        labels = inputs.get("labels")
        outputs = model(**inputs)
        loss_fct = torch.nn.CrossEntropyLoss(weight=self.class_weights.to(model.device))
        loss = loss_fct(outputs.logits.view(-1, self.model.config.num_labels), labels.view(-1))
        return (loss, outputs) if return_outputs else loss

def main():
    print("🧹 Analisis Dataset Emergency...")
    df = pd.read_csv(DATA_PATH, sep=';').dropna()
    
    df['text'] = df['text'].astype(str).apply(preprocess_text)
    df = df[df['text'].str.len() > 10]
    df = df.drop_duplicates(subset=['text'])
    df["label"] = df["label"].astype(int)
    
    print(f"📊 Sisa Data Unik Siap Latih: {len(df)} baris")
    
    train_df, val_df = train_test_split(df, test_size=0.2, stratify=df["label"], random_state=42)
    weights = compute_class_weight("balanced", classes=np.unique(train_df["label"]), y=train_df["label"])
    
    tokenizer = AutoTokenizer.from_pretrained(BASE_MODEL)
    model = AutoModelForSequenceClassification.from_pretrained(BASE_MODEL, num_labels=2, hidden_dropout_prob=0.3)

    # BEKUKAN 100% OTAK BERT
    for param in model.bert.parameters():
        param.requires_grad = False
        
    trainable_params = sum(p.numel() for p in model.parameters() if p.requires_grad)
    print(f"🔒 Layer BERT dikunci! Hanya melatih {trainable_params} parameter (Aman dari Overfitting)")

    def tok(x): return tokenizer(x["text"], truncation=True, max_length=128)
    train_ds = Dataset.from_pandas(train_df).map(tok, batched=True)
    val_ds = Dataset.from_pandas(val_df).map(tok, batched=True)

    args = TrainingArguments(
        output_dir="./tmp_emg", eval_strategy="epoch", save_strategy="epoch",
        load_best_model_at_end=True, metric_for_best_model="f1",
        per_device_train_batch_size=16, num_train_epochs=25,
        learning_rate=2e-3, weight_decay=0.1, warmup_ratio=0.1,
        report_to="none"
    )

    trainer = WeightedTrainer(
        model=model, args=args, train_dataset=train_ds, eval_dataset=val_ds,
        data_collator=DataCollatorWithPadding(tokenizer), compute_metrics=compute_metrics,
        callbacks=[EarlyStoppingCallback(early_stopping_patience=4)]
    )
    trainer.class_weights = torch.tensor(weights, dtype=torch.float)

    trainer.train()
    if os.path.exists(MODEL_DIR): shutil.rmtree(MODEL_DIR)
    model.save_pretrained(MODEL_DIR); tokenizer.save_pretrained(MODEL_DIR)
    print("✅ Emergency Model Bebas Overfitting Berhasil Disimpan!")

if __name__ == "__main__": main()