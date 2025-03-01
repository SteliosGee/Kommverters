import os
import subprocess
import platform
import tempfile
from pathlib import Path

# Dictionary mapping file extensions to their document types
DOCUMENT_FORMATS = {
    'doc': 'word',
    'docx': 'word',
    'pdf': 'pdf',
    'txt': 'text',
    'rtf': 'rtf',
    'odt': 'odt'
}

def convert_document(input_path, output_path, target_format):
    """
    Convert documents between various formats using appropriate libraries
    - PDF to DOCX conversion using pdf2docx
    - DOCX/DOC to PDF conversion using docx2pdf
    """
    input_ext = os.path.splitext(input_path)[1].lower().lstrip('.')
    target_format = target_format.lower()
    
    # Validate formats
    if input_ext not in DOCUMENT_FORMATS:
        raise ValueError(f"Unsupported input format: {input_ext}")
    
    if target_format not in DOCUMENT_FORMATS:
        raise ValueError(f"Unsupported target format: {target_format}")
    
    # Handle different conversion scenarios
    try:
        # PDF to DOCX conversion
        if input_ext == 'pdf' and target_format == 'docx':
            return pdf_to_docx(input_path, output_path)
        
        # DOCX/DOC to PDF conversion
        elif input_ext in ['docx', 'doc'] and target_format == 'pdf':
            return doc_to_pdf(input_path, output_path)
        
        # Other conversions can be added here
        else:
            raise ValueError(f"Conversion from {input_ext} to {target_format} not supported yet")
    
    except Exception as e:
        print(f"Conversion failed: {e}")
        raise

def pdf_to_docx(input_path, output_path):
    """Convert PDF to DOCX using pdf2docx"""
    try:
        # Import here to avoid dependency issues if not needed
        from pdf2docx import Converter
        
        # Convert PDF to DOCX
        cv = Converter(input_path)
        cv.convert(output_path)
        cv.close()
        return True
    except ImportError:
        # Provide instructions if pdf2docx is not installed
        raise ImportError("pdf2docx package is required. Install it with: pip install pdf2docx")

def doc_to_pdf(input_path, output_path):
    """Convert DOC/DOCX to PDF using docx2pdf"""
    try:
        # Import here to avoid dependency issues if not needed
        from docx2pdf import convert
        
        # Convert DOCX to PDF
        convert(input_path, output_path)
        return True
    except ImportError:
        # Provide instructions if docx2pdf is not installed
        raise ImportError("docx2pdf package is required. Install it with: pip install docx2pdf")

def get_document_info(file_path):
    """Get basic information about the document file"""
    info = {
        'file_size': os.path.getsize(file_path),
        'format': os.path.splitext(file_path)[1].lower().lstrip('.'),
        'filename': os.path.basename(file_path)
    }
    return info