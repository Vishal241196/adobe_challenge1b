# utils.py
import re

def clean_text(text):
    text = re.sub(r"\s+", " ", text)
    text = text.strip()
    return text

def chunk_text(text, max_tokens=250):
    words = text.split()
    return [" ".join(words[i:i+max_tokens]) for i in range(0, len(words), max_tokens)]
