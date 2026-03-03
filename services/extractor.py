import fitz  # PyMuPDF
import pdfplumber
from docx import Document
import os

def extract_text_from_pdf(file_path):
    """Extracts text from a PDF file using PyMuPDF with pdfplumber fallback."""
    text = ""
    try:
        print(f"--- Extracting from: {file_path}")
        doc = fitz.open(file_path)
        print(f"--- PyMuPDF: PDF has {len(doc)} pages")
        
        for i, page in enumerate(doc):
            page_text = page.get_text().strip()
            
            # If PyMuPDF is empty, try to detect if it's an image
            if not page_text:
                images = page.get_images(full=True)
                if images:
                    print(f"--- Page {i+1} has {len(images)} images but no text.")
            
            text += page_text + "\n"
        doc.close()

        # If PyMuPDF failed to extract anything, try pdfplumber
        if not text.strip():
            print("--- PyMuPDF failed, trying pdfplumber...")
            with pdfplumber.open(file_path) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
        
        extracted_len = len(text.strip())
        print(f"--- Total extracted: {extracted_len} characters")
        
        if extracted_len == 0:
            print("WARNING: Extracted text is empty. PDF might be an image/scan.")
            
    except Exception as e:
        print(f"Error extracting PDF: {e}")
    return text.strip()

def extract_text_from_docx(file_path):
    """Extracts text from a DOCX file using python-docx."""
    text = ""
    try:
        doc = Document(file_path)
        for para in doc.paragraphs:
            text += para.text + "\n"
    except Exception as e:
        print(f"Error extracting DOCX: {e}")
    return text

def extract_text_from_txt(file_path):
    """Extracts text from a TXT file."""
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            return f.read()
    except Exception as e:
        print(f"Error extracting TXT: {e}")
        return ""

def extract_content(file_path):
    """General extractor based on file extension."""
    ext = os.path.splitext(file_path)[1].lower()
    if ext == '.pdf':
        return extract_text_from_pdf(file_path)
    elif ext == '.docx':
        return extract_text_from_docx(file_path)
    elif ext in ['.txt', '.md']:
        return extract_text_from_txt(file_path)
    else:
        return "Unsupported file format."
