from flask import Blueprint, request, jsonify
from app.services.rag import RAGService
from app.config import Config
from app.services.kb import embedding_model

kb_bp = Blueprint('kb', __name__, url_prefix='/kb')
rag = RAGService(
    url=Config.QDRANT_URL,
    api_key=Config.QDRANT_API_KEY,
    collection="law_docs"
)

@kb_bp.route('/upsert', methods=['POST'])
def upsert():
    data = request.get_json()
    # expect list of docs
    rag.upsert_docs(data['docs'])
    return jsonify(msg="Upserted"), 200