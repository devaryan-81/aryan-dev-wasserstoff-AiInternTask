from pdf2image import convert_from_path
# This function converts each page of a PDF to an image (for OCR-based PDFs)

from app.core.ocr_utils import extract_text_from_image
# We’ll use the OCR function from ocr_utils.py to read text from the images

def extract_text_from_pdf(pdf_path: str) -> str:
    """
    Extract text from scanned PDF using OCR on each page image.

    Args:
        pdf_path (str): Path to the PDF file.

    Returns:
        str: Full extracted text from all pages.
    """
    try:
        # Convert all pages to a list of PIL images
        images = convert_from_path(pdf_path)
        print(f"Converted {len(images)} pages to images.")

        text = ""  # Initialize a variable to store all the text

        for i, img in enumerate(images):
            print(f"Running OCR on page {i+1}...")

            # Use our OCR function to get text from the image
            page_text = extract_text_from_image(img)

            # Add the extracted page text to our final output
            text += page_text + "\n"

        return text.strip()  # Remove any trailing whitespace and return the result

    except Exception as e:
        print(f"[ERROR] Scanned PDF OCR failed: {e}")
        return ""  # Return an empty string if something goes wrong
