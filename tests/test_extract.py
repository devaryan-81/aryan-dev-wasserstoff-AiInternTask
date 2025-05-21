from app.core.pdf_utils import extract_text_from_pdf
from app.core.ocr_utils import extract_text_from_image

# Provide paths to sample files for testing
pdf_path = "backend\data\sample.pdf"
img_path = "backend\data\sample.jpg"



print("PDF TEXT:")
print(extract_text_from_pdf(pdf_path))  # Call the PDF extractor function

print("\nIMAGE OCR TEXT:")
print(extract_text_from_image(img_path))  # Call the image OCR function
