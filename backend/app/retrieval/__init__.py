from pathlib import Path

# index.faiss里面存的主要是每个chunk的embedding向量以及查找用的数据结构，用于快速找到相似内容
# metadata.pkl存每个chunk的原始信息，把查询到的embedding向量还原成文本内容，比如这个文本在第几页，来自哪个文档等
DATA_PATH = Path("data/processed/chunks.jsonl")
INDEX_PATH = Path("data/processed/index.faiss")
METADATA_PATH = Path("data/processed/metadata.pkl")
MODEL_NAME = "BAAI/bge-small-zh-v1.5"