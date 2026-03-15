import pickle
from pathlib import Path
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

from . import INDEX_PATH, METADATA_PATH, MODEL_NAME

class VectorStore:
    def __init__(self):
        self.model = SentenceTransformer(MODEL_NAME)
        self.index = faiss.read_index(str(INDEX_PATH))
        with open(METADATA_PATH, "rb") as f:
            self.metadata = pickle.load(f)

    def search(self, query: str, top_k: int = 5):
        q_vec = self.model.encode(
            [query],
            normalize_embeddings=True
        )
        q_vec = np.asarray(q_vec, dtype=np.float32)

        scores, indices = self.index.search(q_vec, top_k)
        results = []
        for score, i in zip(scores[0], indices[0]):
            if i == -1:
                continue
            item = self.metadata[i]
            results.append({
                "score": float(score),
                "doc_id": item.get("doc_id"),
                "chunk_id": item.get("chunk_id"),
                "page": item.get("page"),
                "title": item.get("title", ""),
                "text": item.get("text", "")
            })
        return results
    

if __name__ == "__main__":
    store = VectorStore()
    while True:
        query = input("\n请输入查询（输入 q 退出）：").strip()
        if query.lower() == "q":
            break

        results = store.search(query, top_k=5)

        print("\n检索结果：")
        for i, item in enumerate(results, 1):
            print(f"\n[{i}] score={item['score']:.4f}")
            print(f"title: {item['title']}")
            print(f"chunk_id: {item['chunk_id']}  page: {item['page']}")
            print(f"text: {item['text'][:300]}...")
