import fitz


def extract_text(pdf_path):
    """
    Extract all text from a PDF file.
    """

    document = fitz.open(pdf_path)

    full_text = ""

    for page in document:
        full_text += page.get_text()

    document.close()

    return full_text


def get_metadata(pdf_path):
    """
    Get metadata of the PDF.
    """

    document = fitz.open(pdf_path)

    metadata = document.metadata

    document.close()

    return metadata


def get_page_count(pdf_path):
    """
    Return total number of pages.
    """

    document = fitz.open(pdf_path)

    total_pages = len(document)

    document.close()

    return total_pages