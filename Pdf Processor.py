import fitz
import os

class PDFProcessor:
    def __init__(self):
        self.loaded_pdfs = {}
    
    def extract_text(self, pdf_path):
        try:
            doc = fitz.open(pdf_path)
            return "".join([page.get_text() for page in doc])
        except: return ""
    
    def load_pdf(self, pdf_path):
        pdf_name = os.path.basename(pdf_path)
        text = self.extract_text(pdf_path)
        self.loaded_pdfs[pdf_name] = text
        return f"✅ PDF loaded: {pdf_name}"