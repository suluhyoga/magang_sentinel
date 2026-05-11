import sys, os, torch
import torch.nn.functional as F
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from core.location_detector import detect_location_advanced
from core.text_preprocessing import preprocess_text

class SentinelAI:
    def __init__(self):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.topic_labels = ["Kriminal", "Lalu Lintas", "Pelayanan", "Sosial", "Lainnya"]
        self.sentiment_labels = ["Negatif", "Netral", "Positif"]
        self.emergency_labels = ["Tidak Darurat", "Darurat"]
        
        # Kata kunci mutlak yang tidak boleh meleset
        self.EMG_VITAL = ["tolong", "darurat", "kecelakaan", "begal", "rampok", "kebakaran", "ledakan"]
        self.load_models()

    def load_models(self):
        print("🧠 Memuat Sentinel AI Core Engine...")
        self.sent_tok = AutoTokenizer.from_pretrained("model/indobert_sentiment")
        self.sent_mod = AutoModelForSequenceClassification.from_pretrained("model/indobert_sentiment").to(self.device).eval()

        self.top_tok = AutoTokenizer.from_pretrained("model/topic_classifier")
        self.top_mod = AutoModelForSequenceClassification.from_pretrained("model/topic_classifier").to(self.device).eval()

        self.emg_tok = AutoTokenizer.from_pretrained("model/emergency_classifier")
        self.emg_mod = AutoModelForSequenceClassification.from_pretrained("model/emergency_classifier").to(self.device).eval()

    @torch.no_grad()
    def _run_inference(self, text, tokenizer, model, labels, threshold=0.4):
        inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True, max_length=128).to(self.device)
        outputs = model(**inputs)
        probs = F.softmax(outputs.logits, dim=1)
        conf, pred = torch.max(probs, dim=1)
        
        if conf.item() < threshold:
            return labels[1] if len(labels) == 3 else "Lainnya", float(conf)
        return labels[pred.item()], float(conf)

    def predict_all(self, text: str):
        # Pembersihan Wajib
        clean_text = preprocess_text(text)
        
        # Jika setelah dibersihkan teksnya kosong, tolak prosesnya
        if not clean_text or len(clean_text.strip()) < 8:
            return None

        sent, s_conf = self._run_inference(clean_text, self.sent_tok, self.sent_mod, self.sentiment_labels)
        topic, t_conf = self._run_inference(clean_text, self.top_tok, self.top_mod, self.topic_labels)
        emg_label, e_conf = self._run_inference(clean_text, self.emg_tok, self.emg_mod, self.emergency_labels, threshold=0.5)

        is_vital = any(word in clean_text.lower() for word in self.EMG_VITAL)
        emergency = 1 if (emg_label == "Darurat" or is_vital) else 0
        location = detect_location_advanced(clean_text)

        # Kembalikan clean_text untuk diamankan ke DB
        return (sent, s_conf, topic, t_conf, emergency, location, clean_text)

ai_engine = SentinelAI()