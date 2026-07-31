from utils.pdf_reader import extract_text
from utils.cleaner import clean_text
from utils.summarizer import summarize_text

pdf_path = "uploads/sample.pdf"

text = extract_text(pdf_path)

cleaned_text = clean_text(text)

summary = summarize_text(cleaned_text)

print(summary)