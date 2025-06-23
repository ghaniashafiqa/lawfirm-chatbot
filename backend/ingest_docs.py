# ingest_docs.py
from app.services.rag import RAGService
from app.utils import parse_pdf
from app.config import Config
from sentence_transformers import SentenceTransformer

embedder = SentenceTransformer("intfloat/multilingual-e5-large")
rag = RAGService(Config.QDRANT_URL, Config.QDRANT_API_KEY)

docs = []
for path in PDF_PATHS:
    text = parse_pdf(path)
    for i, chunk in enumerate(split_text(text)):
        vec = embedder.encode(chunk).tolist()
        docs.append({
            "id": f"{slugify(path)}_{i}",
            "vector": vec,
            "metadata": {"page_content": chunk, "title": ..., "url": ...}
        })
rag.upsert_docs(docs)
