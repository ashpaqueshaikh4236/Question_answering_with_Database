import pdfplumber
import docx

def extract_text_from_pdf(file):
    with pdfplumber.open(file) as pdf:
        text = "".join([page.extract_text() for page in pdf.pages])
    return text

def extract_text_from_docx(file):
    doc = docx.Document(file)
    return "\n".join([para.text for para in doc.paragraphs])

def extract_text_from_txt(file):
    return file.read().decode("utf-8")

def process_file(file, file_type):
    if file_type == 'pdf':
        return extract_text_from_pdf(file)
    elif file_type == 'docx':
        return extract_text_from_docx(file)
    elif file_type == 'txt':
        return extract_text_from_txt(file)
    else:
        raise ValueError("Unsupported file type")