import os

class PDFProcessor:
    def __init__(self):
        self.upload_folder = "uploads"
        os.makedirs(self.upload_folder, exist_ok=True)
    
    def handle_upload(self, file):
        """Handle PDF file upload"""
        if file and file.filename.endswith('.pdf'):
            file_path = os.path.join(self.upload_folder, file.filename)
            file.save(file_path)
            return f"✅ PDF uploaded successfully: {file.filename}"
        return "❌ Please upload a valid PDF file"

pdf_processor = PDFProcessor()
