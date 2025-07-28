# summarizer.py
import os
from transformers import T5Tokenizer, T5ForConditionalGeneration

model_path = os.getenv("T5_PATH", "/app/t5_model")
tokenizer = T5Tokenizer.from_pretrained(model_path)
model = T5ForConditionalGeneration.from_pretrained(model_path)

def summarize_text(text, max_tokens=120):
    input_text = "summarize: " + text
    inputs = tokenizer.encode(input_text, return_tensors="pt", max_length=512, truncation=True)
    summary_ids = model.generate(inputs, max_length=max_tokens, num_beams=4, early_stopping=True)
    summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
    return summary
