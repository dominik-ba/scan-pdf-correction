import fitz  # PyMuPDF
import spacy
from langdetect import detect

# Load spaCy models
nlp_en = spacy.load("en_core_web_sm")
nlp_de = spacy.load("de_core_news_sm")

def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        text += page.get_text()
    return text

def extract_dates(text, lang):
    if lang == 'de':
        doc = nlp_de(text)
    else:
        doc = nlp_en(text)
    dates = [ent.text for ent in doc.ents if ent.label_ == "DATE"]
    return dates

if __name__ == "__main__":
    pdf_path = "path/to/your/pdf_file.pdf"
    text = extract_text_from_pdf(pdf_path)
    lang = detect(text)
    dates = extract_dates(text, lang)
    print("Extracted Dates:", dates)
