import json
from pathlib import Path
from typing import List
from sentence_transformers import SentenceTransformer

from app.config import Config
from app.services.rag import RAGService
from app.utils import parse_pdf

# Text splitter function
def split_text(text: str, chunk_size: int = 1000, chunk_overlap: int = 200) -> List[str]:
    """Simple text splitter"""
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        if end < len(text):
            # Try to break at a sentence or paragraph
            for sep in ['\n\n', '\n', '. ', ' ']:
                last_sep = text.rfind(sep, start, end)
                if last_sep != -1:
                    end = last_sep + len(sep)
                    break
        
        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)
        
        start = end - chunk_overlap if end < len(text) else end
    
    return chunks

def slugify(text: str) -> str:
    """Simple slugify function"""
    import re
    return re.sub(r'[^\w\-_]', '_', text.lower())

def load_documents_from_path(path: str) -> List[dict]:
    """Load documents from various file types"""
    docs = []
    embedder = SentenceTransformer("intfloat/multilingual-e5-large")
    
    for file_path in Path(path).glob("*"):
        suffix = file_path.suffix.lower()
        print(f"📄 Loading: {file_path.name}")
        
        if suffix == ".json":
            # Handle JSON files (like your original script)
            try:
                data = json.loads(file_path.read_text(encoding="utf-8"))
                for i, item in enumerate(data):
                    content = item.get("content", "")
                    if content.strip():
                        chunks = split_text(content)
                        for j, chunk in enumerate(chunks):
                            vector = embedder.encode(chunk).tolist()
                            docs.append({
                                "id": f"{slugify(file_path.stem)}_{i}_{j}",
                                "vector": vector,
                                "metadata": {
                                    "text": chunk,
                                    "source": file_path.name,
                                    "title": item.get("title", ""),
                                    "date": item.get("date", ""),
                                    "slug": item.get("slug", ""),
                                    "url": f"https://gebukmantan.com/{item.get('slug', '')}/"
                                }
                            })
            except Exception as e:
                print(f"Error processing JSON {file_path.name}: {e}")
                
        elif suffix == ".pdf":
            # Handle PDF files
            try:
                text = parse_pdf(str(file_path))
                if text.strip():
                    chunks = split_text(text)
                    for i, chunk in enumerate(chunks):
                        vector = embedder.encode(chunk).tolist()
                        docs.append({
                            "id": f"{slugify(file_path.stem)}_{i}",
                            "vector": vector,
                            "metadata": {
                                "text": chunk,
                                "source": file_path.name,
                                "title": file_path.stem,
                                "file_type": "pdf"
                            }
                        })
            except Exception as e:
                print(f"Error processing PDF {file_path.name}: {e}")
        else:
            print(f"⚠️ Unsupported file: {file_path.name}")
    
    return docs

def main():
    """Main function to run document ingestion"""
    INPUT_PATH = "knowledge/"  # Make sure this directory exists
    
    # Initialize RAG service
    rag = RAGService(Config.QDRANT_URL, Config.QDRANT_API_KEY)
    
    # Load and process documents
    print("🚀 Starting document ingestion...")
    docs = load_documents_from_path(INPUT_PATH)
    
    if docs:
        print(f"📚 Loaded {len(docs)} document chunks")
        
        # Upsert to Qdrant
        rag.upsert_docs(docs)
        print(f"✅ Successfully upserted {len(docs)} chunks to Qdrant")
    else:
        print("❌ No documents found to ingest")

if __name__ == "__main__":
    main()