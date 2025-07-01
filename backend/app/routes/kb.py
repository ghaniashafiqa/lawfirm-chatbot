from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
from app.services.rag import RAGService
from app.services.kb import embedding_model
from app.config import Config
from pathlib import Path
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PDFPlumberLoader
from qdrant_client import QdrantClient
from qdrant_client.http.models import PointStruct
import os, uuid, re

UPLOAD_DIR = "knowledge"
os.makedirs(UPLOAD_DIR, exist_ok=True)

kb_bp = Blueprint('kb', __name__, url_prefix='/kb')
rag = RAGService(Config.QDRANT_URL, Config.QDRANT_API_KEY, Config.COLLECTION_NAME)

@kb_bp.route('/upload', methods=['POST'])
def upload_file_and_upsert():
    file = request.files.get('file')
    description = request.form.get('description', '')

    if not file:
        return jsonify({"error": "No file uploaded"}), 400

    filename = secure_filename(file.filename)
    temp_dir = "temp_uploads"
    os.makedirs(temp_dir, exist_ok=True)
    file_path = os.path.join(temp_dir, f"{uuid.uuid4()}_{filename}")
    file.save(file_path)

    try:
        loader = PDFPlumberLoader(file_path)
        docs = loader.load()

        for doc in docs:
            doc.metadata["source"] = filename
            doc.metadata["description"] = description

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            separators=["\n\n", "\n", ". ", " ", ""],
        )
        chunks = splitter.split_documents(docs)

        qdrant = QdrantClient(url=Config.QDRANT_URL, api_key=Config.QDRANT_API_KEY)
        vectors = [
            PointStruct(
                id=uuid.uuid4().int >> 96,
                vector=embedding_model.encode(chunk.page_content).tolist(),
                payload={**chunk.metadata, "text": chunk.page_content},
            )
            for chunk in chunks
        ]
        qdrant.upsert(collection_name=Config.COLLECTION_NAME, points=vectors)
        return jsonify({"msg": f"Uploaded and upserted {len(chunks)} chunks"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        os.remove(file_path)

@kb_bp.route('/get-data', methods=['GET'])
def get_all_vectors():
    try:
        qdrant = QdrantClient(url=Config.QDRANT_URL, api_key=Config.QDRANT_API_KEY)

        all_points = []
        next_offset = None

        while True:
            result, next_offset = qdrant.scroll(
                collection_name=Config.COLLECTION_NAME,
                scroll_filter=None,
                with_payload=True,
                offset=next_offset
            )
            all_points.extend(result)
            if next_offset is None:
                break

        data = [
            {
                "id": str(p.id),
                "payload": p.payload
            }
            for p in all_points
        ]
        return jsonify(data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@kb_bp.route('/search-data', methods=['GET'])
def search_vectors():
    query = request.args.get('q', '')
    if not query:
        return jsonify({"error": "Missing query param `q`"}), 400

    try:
        qdrant = QdrantClient(url=Config.QDRANT_URL, api_key=Config.QDRANT_API_KEY)

        query_vector = embedding_model.encode(query).tolist()
        search_result = qdrant.search(
            collection_name=Config.COLLECTION_NAME,
            query_vector=query_vector,
            limit=20,
            with_payload=True
        )

        data = [
            {
                "id": str(p.id),
                "score": p.score,
                "payload": p.payload
            }
            for p in search_result
        ]
        return jsonify(data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
