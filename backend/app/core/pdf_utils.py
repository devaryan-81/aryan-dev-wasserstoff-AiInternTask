def extract_text_from_pdf(pdf_path: str) -> str:
    try:
        from pdf2image import convert_from_path
        from app.core.ocr_utils import extract_text_from_image
        from PyPDF2 import PdfReader

        text = ""
        reader = PdfReader(pdf_path)
        for i in range(len(reader.pages)):
            images = convert_from_path(pdf_path, first_page=i+1, last_page=i+1, dpi=200)
            text += extract_text_from_image(images[0]) + "\n"
        return text.strip()

    except Exception as e:
        print(f"[ERROR] PDF OCR failed: {e}")
        # 🔁 Fallback for text-based PDFs
        try:
            import pdfplumber
            with pdfplumber.open(pdf_path) as pdf:
                return "\n".join([p.extract_text() or "" for p in pdf.pages])
        except Exception as e2:
            print(f"[FALLBACK ERROR] pdfplumber failed: {e2}")
            return ""
