from flask import Blueprint, request, jsonify
from app.config import Config
from app.services.rag import RAGService
from app.services.llm import DeepseekClient
from app.services.kb import embedding_model
from app.db import db
from app.models import ChatHistory

chat_bp = Blueprint("chat", __name__, url_prefix="/chat")

# instantiate with your config
rag = RAGService(Config.QDRANT_URL, Config.QDRANT_API_KEY)
llm = DeepseekClient(Config.DEEPSEEK_API_KEY)

@chat_bp.route("", methods=["POST"])
def chat():
    data = request.get_json(force=True)
    query = data["question"]
    # 1) embed
    q_vec = embedding_model.encode(query).tolist()
    # 2) retrieve
    hits = rag.query(q_vec)
    context = "\n\n".join(hit.payload["page_content"] for hit in hits)
    # 3) generate
    prompt = f"Context:\n{context}\n\nUser: {query}\nBot:"
    answer = llm.generate(prompt)

    # 4) save to DB
    session_id = data.get("session_id", None)
    record = ChatHistory(session_id=session_id, question=query, answer=answer)
    db.session.add(record)
    db.session.commit()

    return jsonify(answer=answer), 200
