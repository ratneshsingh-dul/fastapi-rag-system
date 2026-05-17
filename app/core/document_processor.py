import io
import re

from pathlib import Path
from typing import List, Tuple

import pypdf
import docx

from app.core.config import settings


def extract_text_from_pdf(content: bytes) -> Tuple[str, int]:

    reader = pypdf.PdfReader(io.BytesIO(content))

    pages = []

    for page in reader.pages:
        text = page.extract_text() or ""
        pages.append(text)

    return "\n\n".join(pages), len(reader.pages)


def extract_text_from_docx(content: bytes) -> Tuple[str, int]:

    document = docx.Document(io.BytesIO(content))

    paragraphs = [
        p.text for p in document.paragraphs
        if p.text.strip()
    ]

    word_count = sum(len(p.split()) for p in paragraphs)

    estimated_pages = max(1, word_count // 300)

    return "\n\n".join(paragraphs), estimated_pages


def extract_text_from_txt(content: bytes) -> Tuple[str, int]:

    text = content.decode(
        "utf-8",
        errors="replace",
    )

    estimated_pages = max(
        1,
        len(text.split()) // 300,
    )

    return text, estimated_pages


def extract_text(filename: str, content: bytes):

    ext = Path(filename).suffix.lower()

    if ext == ".pdf":
        return extract_text_from_pdf(content)

    elif ext in (".docx", ".doc"):
        return extract_text_from_docx(content)

    elif ext in (".txt", ".md"):
        return extract_text_from_txt(content)

    raise ValueError(f"Unsupported file type: {ext}")


def clean_text(text: str) -> str:

    text = re.sub(r"\n{3,}", "\n\n", text)

    text = re.sub(r" {2,}", " ", text)

    return text.strip()


def chunk_text(
    text: str,
    chunk_size: int = settings.CHUNK_SIZE,
    overlap: int = settings.CHUNK_OVERLAP,
) -> List[str]:

    text = clean_text(text)

    if not text:
        return []

    chunks = []

    start = 0

    while start < len(text):

        end = start + chunk_size

        chunk = text[start:end]

        chunks.append(chunk)

        start += chunk_size - overlap

    return chunks