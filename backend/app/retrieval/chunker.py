def split_text(text: str, chunk_size: int = 800, overlap: int = 100):
    # overlap可以防止语义截断与信息丢失、提升检索的准确率
    text = text.strip()
    if not text:
        return []
    chunks = []
    start = 0
    n = len(text)
    while start < n:
        end = min(start + chunk_size, n)
        chunk = text[start: end].strip()
        if chunk:
            chunks.append(chunk)
        if end == n:
            break
        start = max(end - overlap, start + 1)
    return chunks