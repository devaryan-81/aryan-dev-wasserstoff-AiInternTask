from PIL import Image
# PIL (Pillow) is used to open and manipulate images

import pytesseract
# pytesseract is the Python wrapper for the Tesseract OCR engine

def extract_text_from_image(image_path_or_object):
    """
    Extract text from an image using Tesseract OCR.
    Handles both image file paths and PIL Image objects.

    Args:
        image_path_or_object (str or Image): Image path or PIL Image.

    Returns:
        str: Extracted text.
    """
    try:
        # If the input is a file path, open the image; else assume it’s a PIL Image object
        image = Image.open(image_path_or_object) if isinstance(image_path_or_object, str) else image_path_or_object

        # Convert the image to grayscale to improve OCR accuracy
        image = image.convert('L')

        # Resize the image to double the size to make text more readable by OCR
        image = image.resize((image.width * 2, image.height * 2))

        print(f"Image size after resize: {image.size}")

        # Perform OCR on the processed image
        text = pytesseract.image_to_string(image)

        print(f"OCR output: {text[:100]}")  # Print a preview of the output

        return text.strip()  # Return the cleaned-up text

    except Exception as e:
        print(f"[ERROR] OCR failed: {e}")
        return ""  # Return empty if there is any error
