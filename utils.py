# utils.py
import io
from typing import Optional
from PyPDF2 import PdfReader
import docx


def extract_text_from_pdf(file_bytes: bytes) -> str:
    with io.BytesIO(file_bytes) as f:
        reader = PdfReader(f)
        pages = [page.extract_text() or "" for page in reader.pages]
    return "\n\n".join(pages)


def extract_text_from_docx(file_bytes: bytes) -> str:
    with io.BytesIO(file_bytes) as f:
        document = docx.Document(f)
        paragraphs = [p.text for p in document.paragraphs]
    return "\n".join(paragraphs)


def extract_text_from_upload(uploaded_file) -> Optional[str]:
    """
    Recibe el objeto de Streamlit (st.file_uploader) y extrae texto
    según la extensión.
    """
    if uploaded_file is None:
        return None

    file_bytes = uploaded_file.read()
    name = uploaded_file.name.lower()

    if name.endswith(".pdf"):
        return extract_text_from_pdf(file_bytes)
    elif name.endswith(".docx"):
        return extract_text_from_docx(file_bytes)
    elif name.endswith(".txt"):
        return file_bytes.decode("utf-8", errors="ignore")
    else:
        return None
