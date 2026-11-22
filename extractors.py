from pathlib import Path
from io import BytesIO
from pypdf import PdfReader
from docx import Document

SUPPORTED = {".pdf", ".docx", ".txt"}

def extract_text(filename: str, content: bytes) -> str:
    """Extract readable text from a PDF, DOCX, or TXT file."""
    suffix = Path(filename).suffix.lower()
    if suffix not in SUPPORTED:
        raise ValueError(f"Unsupported file type: {suffix}")

    if suffix == ".txt":
        return content.decode("utf-8", errors="replace")

    if suffix == ".pdf":
        reader = PdfReader(BytesIO(content))
        return "\n".join(page.extract_text() or "" for page in reader.pages)

    document = Document(BytesIO(content))
    paragraphs = [p.text for p in document.paragraphs if p.text.strip()]
    for table in document.tables:
        for row in table.rows:
            paragraphs.append(" | ".join(cell.text for cell in row.cells))
    return "\n".join(paragraphs)
