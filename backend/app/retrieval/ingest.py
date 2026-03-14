import json
from pathlib import Path
from tqdm import tqdm

from ..tools.id_gen import get_id
from .loaders import load_markdown, load_pdf, load_txt
from .cleaner import clean_text
from .chunker import split_text

def load_doc(path: str | Path) -> dict:
    suffix = path.suffix.lower()
    if suffix == ".pdf":
        return load_pdf(path)
    if suffix == ".txt":
        return load_txt(path)
    if suffix == ".md":
        return load_markdown(path)
    
    raise ValueError(f"不支持的文件格式：{suffix}")

def doc_to_chunks(doc: dict, doc_id: str, chunk_size: int=800, overlap: int=100):
    chunk_records = []
    chunk_idx = 1

    for page_item in doc["pages"]:
        page_num = page_item["page"]
        cleaned = clean_text(page_item["text"])
        if not cleaned:
            continue
        chunks = split_text(text=cleaned, chunk_size=chunk_size, overlap=overlap)
        for chunk in chunks:
            chunk_records.append({
                "doc_id": doc_id,
                "chunk_id": f"{doc_id}_{chunk_idx}",
                "title": doc["title"],
                "page": page_num,
                "source_path": doc["source_path"],
                "file_type": doc["file_type"],
                "text": chunk
            })
            chunk_idx += 1

    return chunk_records

def main():
    raw_dir = Path("data/raw")
    out_dir = Path("data/processed")
    out_dir.mkdir(parents=True, exist_ok=True)
    all_chunks = []
    manifest = {
        "total_docs": 0,
        "total_chunks": 0,
        "success_docs": [],
        "failed_docs": []
    }

    files = sorted([p for p in raw_dir.iterdir() if p.is_file()])
    for idx, path in enumerate(tqdm(files), start=1):
        doc_id = get_id()
        try:
            doc = load_doc(path=path)
            chunks = doc_to_chunks(doc=doc, doc_id=doc_id)
            all_chunks.extend(chunks)

            manifest["success_docs"].append({
                "doc_id": doc_id,
                "title": doc["title"],
                "source_path": str(path),
                "num_chunks": len(chunks)
            })
        except Exception as e:
            manifest["failed_docs"].append({
                "source_path": str(path),
                "error": str(e)
            })

    manifest["total_docs"] = len(files)
    manifest["total_chunks"] = len(all_chunks)

    chunks_path = out_dir / "chunks.jsonl"
    with chunks_path.open("w", encoding="utf-8") as f:
        for item in all_chunks:
            # 允许直接将中文以字符形式写入文件，加换行符方便流式读取
            f.write(json.dumps(item, ensure_ascii=False) + "\n")
    
    manifest_path = out_dir / "manifest.json"
    manifest_path.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )

    print(f"Saved {len(all_chunks)} chunks to {chunks_path}")
    print(f"Saved manifest to {chunks_path}")


if __name__ == "__main__":
    main()
