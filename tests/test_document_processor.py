from app.core.document_processor import (
    extract_text_from_txt,
    clean_text,
    chunk_text,
)


def test_clean_text():

    text = "Hello     World"

    cleaned = clean_text(text)

    assert "  " not in cleaned


def test_chunk_text():

    text = "Hello world " * 500

    chunks = chunk_text(text)

    assert len(chunks) > 0


def test_extract_text():

    content = b"Hello World"

    text, pages = extract_text_from_txt(
        content
    )

    assert "Hello" in text

    assert pages >= 1