from utils.pdf_reader import extract_text, get_metadata
from utils.cleaner import clean_text

pdf_path = "uploads/sample.pdf"

# Extract text
text = extract_text(pdf_path)

# Clean text
cleaned_text = clean_text(text)

# Metadata
metadata = get_metadata(pdf_path)

print("=" * 50)
print("METADATA")
print("=" * 50)
print(metadata)

print("\n" + "=" * 50)
print("CLEANED TEXT")
print("=" * 50)

print(cleaned_text[:1000])