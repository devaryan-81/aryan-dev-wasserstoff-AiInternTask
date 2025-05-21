from PIL import Image
import pytesseract

def extract_text_from_image(image_path_or_object):
    try:
        # Open image from path or object
        image = Image.open(image_path_or_object) if isinstance(image_path_or_object, str) else image_path_or_object

        # Convert to grayscale
        image = image.convert("L")

        # Resize if too large
        max_width, max_height = 2000, 2000
        if image.width > max_width or image.height > max_height:
            ratio = min(max_width / image.width, max_height / image.height)
            new_size = (int(image.width * ratio), int(image.height * ratio))
            image = image.resize(new_size)
            print(f"Image size after resize: {image.size}")

        # Run OCR
        text = pytesseract.image_to_string(image)
        return text.strip()

    except Exception as e:
        print(f"[ERROR] OCR failed: {e}")
        return ""
