import re

# Kata kasar tidak dihapus agar AI bisa deteksi emosi negatif (Kriminal/Sosial)
BAD_WORDS = ["anjing", "bangsat", "tolol", "kontol", "memek"]

def remove_url(text):
    # Regex yang jauh lebih agresif untuk menangkap semua jenis URL
    return re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', text)

def remove_mention(text):
    # Menghapus @username secara tuntas
    return re.sub(r'@[\w\.-]+', '', text)

def remove_hashtag(text):
    return re.sub(r'#(\w+)', r'\1', text)

def remove_emoji(text):
    return re.sub(r'[^\w\s.,!?\-]', '', text)

def normalize_repeated_chars(text):
    return re.sub(r'(.)\1{2,}', r'\1\1', text)

def normalize_whitespace(text):
    return re.sub(r'\s+', ' ', text).strip()

def preprocess_text(text: str) -> str:
    if not text:
        return ""

    text = remove_url(text)
    text = remove_mention(text)
    text = remove_hashtag(text)
    text = remove_emoji(text)
    text = normalize_repeated_chars(text)
    
    text = text.lower()
    text = normalize_whitespace(text)

    return text