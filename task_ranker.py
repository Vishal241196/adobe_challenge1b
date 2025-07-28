# task_ranker.py
from sentence_transformers import SentenceTransformer, util
import os

# Load multilingual sentence transformer (<=100MB, offline)
model_path = os.getenv("MODEL_PATH", "sentence-transformers/distiluse-base-multilingual-cased-v1")
model = SentenceTransformer(model_path)

def rank_sections(query, sections, top_k=5):
    query_embedding = model.encode(query, convert_to_tensor=True)
    scored = []
    for sec in sections:
        sec_embedding = model.encode(sec["text"], convert_to_tensor=True)
        score = util.cos_sim(query_embedding, sec_embedding).item()
        scored.append({ **sec, "score": score })
    top = sorted(scored, key=lambda x: x["score"], reverse=True)[:top_k]
    return top
