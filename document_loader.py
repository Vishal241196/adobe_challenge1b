# document_loader.py
import fitz  # PyMuPDF

def extract_sections_from_pdf(filepath):
    doc = fitz.open(filepath)
    sections = []
    for page_num in range(len(doc)):
        page = doc[page_num]
        text = page.get_text()
        # Naive paragraph split
        paragraphs = [p.strip() for p in text.split("\n\n") if len(p.strip()) > 50]
        for para in paragraphs:
            sections.append({
                "text": para,
                "page_number": page_num + 1
            })
    doc.close()
    return sections
