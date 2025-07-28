# extractor.py
import os
import json
from document_loader import extract_sections_from_pdf
from task_ranker import rank_sections
from summarizer import summarize_text
from datetime import datetime

import os

input_dir = "/app/input/pdf"
input_json = "/app/input/challenge1b_input.json"
output_json = "/app/output/output_1b.json"


def main():

    with open(input_json, "r") as f:
        input_data = json.load(f)

    persona = input_data["persona"]["role"]
    job_task = input_data["job_to_be_done"]["task"]
    prompt = f"As a {persona}, your job is: {job_task}"
     
    all_sections = []
    for doc in input_data["documents"]:
        filename = doc["filename"]
        path = os.path.join(input_dir, filename)
        if not os.path.exists(path):
            continue
        sections = extract_sections_from_pdf(path)
        for sec in sections:
            sec["document"] = filename
        all_sections.extend(sections)

    # RAG-lite similarity
    top_sections = rank_sections(prompt, all_sections, top_k=5)

    extracted_sections = []
    subsection_analysis = []
    for i, sec in enumerate(top_sections):
        extracted_sections.append({
            "document": sec["document"],
            "section_title": sec["text"][:100],
            "importance_rank": i + 1,
            "page_number": sec["page_number"]
        })
        subsection_analysis.append({
            "document": sec["document"],
            "refined_text": summarize_text(sec["text"]),
            "page_number": sec["page_number"]
        })

    output = {
        "metadata": {
            "input_documents": [d["filename"] for d in input_data["documents"]],
            "persona": persona,
            "job_to_be_done": job_task,
            "processing_timestamp": datetime.now().isoformat()
        },
        "extracted_sections": extracted_sections,
        "subsection_analysis": subsection_analysis
    }

    with open(output_json, "w") as f:
        json.dump(output, f, indent=2)

    print(f"✅ Extracted → {output_json}")


if __name__ == "__main__":
    main()
