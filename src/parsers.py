"""Read TXT, PDF and DOCX in memory; files are not saved."""
from io import BytesIO
from pypdf import PdfReader
from docx import Document


def extract_document(filename: str, contents: bytes) -> str:
    extension = filename.rsplit('.', 1)[-1].lower()
    if len(contents) > 5_000_000:
        raise ValueError("Maximum file size is 5 MB.")
    if extension == 'txt':
        return contents.decode('utf-8-sig')
    if extension == 'pdf':
        return '\n'.join(page.extract_text() or '' for page in PdfReader(BytesIO(contents)).pages)
    if extension == 'docx':
        return '\n'.join(p.text for p in Document(BytesIO(contents)).paragraphs)
    raise ValueError("Supported formats: .txt, .pdf, .docx")
