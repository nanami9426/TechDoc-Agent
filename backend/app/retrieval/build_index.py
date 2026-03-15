import json
import pickle
from pathlib import Path
import faiss
from sentence_transformers import SentenceTransformer
import numpy as np
from tqdm import tqdm

# index.faiss里面存的主要是每个chunk的embedding向量以及查找用的数据结构，用于快速找到相似内容
# metadata.pkl存每个chunk的原始信息，把查询到的embedding向量还原成文本内容，比如这个文本在第几页，来自哪个文档等
DATA_PATH = Path("data/processed/chunks.jsonl")
INDEX_PATH = Path("data/processed/index.faiss")
METADATA_PATH = Path("data/processed/metadata.pkl")
MODEL_NAME = "BAAI/bge-small-zh-v1.5"

def load_chunks(path: str | Path) -> list:
    # 读取jsonl
    chunks = []
    with open(path, "r", encoding="utf8") as f:
        for i, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            try:
                item = json.loads(line)
                if "text" not in item:
                    print(f"[WARN] {path}第{i}行没有'text'属性，跳过")
                    continue
                chunks.append(item)
            except Exception as e:
                print(f"[WARN] {path}第{i}行读取失败，{e}")
    return chunks

def main():
    chunks = load_chunks(path=DATA_PATH)
    texts = [item["text"] for item in chunks]
    print(f"加载了 {len(chunks)} 条chunk")

    model = SentenceTransformer(MODEL_NAME)
    embeddings = model.encode(
        texts,
        batch_size=32,
        show_progress_bar=True,
        normalize_embeddings=True
    )
    embeddings = np.asarray(embeddings, dtype=np.float32)
    dim = embeddings.shape[1]

    # 构建索引
    index = faiss.IndexFlatIP(dim)
    index.add(embeddings)
    faiss.write_index(index, str(INDEX_PATH))

    with open(METADATA_PATH, "wb") as f:
        pickle.dump(chunks, f)

    print(f"embeddings shape: {embeddings.shape}")
    print(f"索引文件保存在 {INDEX_PATH}")
    print(f"元数据保存在 {METADATA_PATH}")

if __name__ == "__main__":
    main()