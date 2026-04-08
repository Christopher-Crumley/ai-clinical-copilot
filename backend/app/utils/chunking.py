from typing import List


def chunk_text(
    text: str,
    chunk_size: int = 500,
    overlap: int = 75,
) -> List[str]:
    """
    Split text into overlapping word-based chunks.

    Args:
        text:       Raw document text.
        chunk_size: Approximate words per chunk.
        overlap:    Words shared between adjacent chunks.

    Returns:
        List of string chunks.
    """
    words = text.split()
    chunks: List[str] = []
    start = 0

    while start < len(words):
        end = min(start + chunk_size, len(words))
        chunk = " ".join(words[start:end])
        chunks.append(chunk)
        if end == len(words):
            break
        start += chunk_size - overlap

    return chunks


def chunk_by_paragraph(text: str, max_words: int = 400) -> List[str]:
    """
    Split text by paragraph boundaries, merging short paragraphs
    and splitting long ones. Useful for structured clinical notes.
    """
    paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
    chunks: List[str] = []
    current: List[str] = []
    current_words = 0

    for para in paragraphs:
        para_words = len(para.split())
        if current_words + para_words > max_words and current:
            chunks.append("\n\n".join(current))
            current = []
            current_words = 0
        current.append(para)
        current_words += para_words

    if current:
        chunks.append("\n\n".join(current))

    return chunks
