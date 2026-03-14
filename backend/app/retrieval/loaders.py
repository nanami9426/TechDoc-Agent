from pathlib import Path
import fitz # pymupdf

def load_pdf(path: str | Path) -> dict:
    pages = []
    doc = fitz.open(path)
    metadata = doc.metadata or {}
    title = metadata.get("title")
    if title:
        title = title.strip()
    else:
        title = Path(path).stem
    for i, page in enumerate(doc):
        text = page.get_text()
        pages.append({
            "page": i + 1,
            "text": text
        })
    return {
        "source_path": str(path),
        "file_type": "pdf",
        "title": title,
        "pages": pages
    }

def load_markdown(path: str | Path) -> dict:
    text = Path(path).read_text(encoding="utf8", errors="ignore")
    return {
        "source_path": str(path),
        "file_type": "md",
        "title": Path(path).stem,
        "pages": [{"page": 1, "text": text}]
    }

def load_txt(path: str | Path) -> dict:
    text = Path(path).read_text(encoding="utf8", errors="ignore")
    return {
        "source_path": str(path),
        "file_type": "txt",
        "title": Path(path).stem,
        "pages": [{"page": 1, "text": text}]
    }