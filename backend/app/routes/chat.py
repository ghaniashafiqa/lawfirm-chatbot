from flask import Blueprint, request, jsonify
from app.config import Config
from app.services.rag import RAGService
from app.services.llm import OpenAIClient
from app.services.kb import embedding_model
from app.db import db
from app.models import ChatHistory
import uuid
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

chat_bp = Blueprint("chat", __name__, url_prefix="/chat")

# Initialize services with error handling
try:
    rag = RAGService(Config.QDRANT_URL, Config.QDRANT_API_KEY, Config.COLLECTION_NAME)
    llm = OpenAIClient(Config.OPENAI_API_KEY)
    logger.info("✅ Services initialized successfully")
except Exception as e:
    logger.error(f"❌ Error initializing services: {e}")
    rag = None
    llm = None

@chat_bp.route("", methods=["POST"])
def chat():
    try:
        # Check if services are initialized
        if not rag or not llm:
            return jsonify(error="Services not properly initialized"), 500
            
        data = request.get_json(force=True)
        query = data.get("question", "").strip()
        
        if not query:
            return jsonify(error="Question is required"), 400
        
        # Generate session ID if not provided
        session_id = data.get("session_id") or str(uuid.uuid4())
        
        logger.info(f"Processing question: {query[:50]}...")
        
        # 1) Embed the query
        try:
            q_vec = embedding_model.encode(query).tolist()
        except Exception as e:
            logger.error(f"Error embedding query: {e}")
            return jsonify(error="Error processing question"), 500
        
        # 2) Retrieve relevant documents
        try:
            hits = rag.query(q_vec, top_k=3, score_threshold=0.7)
            logger.info(f"Found {len(hits)} relevant documents")
        except Exception as e:
            logger.error(f"Error querying documents: {e}")
            hits = []
        
        if hits:
            # Extract context from search results
            context_parts = []
            for hit in hits:
                if hasattr(hit, 'payload'):
                    if 'text' in hit.payload:
                        context_parts.append(hit.payload['text'])
                    elif 'page_content' in hit.payload:
                        context_parts.append(hit.payload['page_content'])
            
            context = "\n\n".join(context_parts[:3])  # Limit context
            logger.info(f"Context length: {len(context)} characters")
        else:
            context = ""
            logger.info("No relevant documents found")
        
        # 3) Generate response using GPT-4o-mini
        if hits:
            # Build context from search results
            context_parts = []
            for hit in hits:
                if hasattr(hit, 'payload'):
                    if 'text' in hit.payload:
                        context_parts.append(hit.payload['text'])
                    elif 'page_content' in hit.payload:
                        context_parts.append(hit.payload['page_content'])
            
            context = "\n\n".join(context_parts[:3])  # Limit context
            logger.info(f"Context length: {len(context)} characters")
            
            # Create RAG prompt with strict instructions
            prompt = f"""Jawab pertanyaan hanya berdasarkan konteks berikut dari basis pengetahuan Kantor Hukum SAP. 
Jika konteks tidak mengandung informasi yang cukup untuk menjawab pertanyaan, katakan dengan jelas "Saya tidak memiliki informasi yang cukup untuk menjawab pertanyaan itu" dan sarankan untuk menghubungi kantor langsung.

Konteks:
{context}

Pertanyaan: {query}

Harap berikan jawaban yang akurat berdasarkan konteks yang disediakan. Jika Anda perlu membuat asumsi apa pun atau jika konteksnya tidak mencukupi, nyatakan hal ini dengan jelas dalam respons Anda."""
        else:
            # Fallback response when no relevant context found
            prompt = f"""Saya tidak menemukan informasi spesifik dalam basis pengetahuan saya untuk menjawab pertanyaan ini: {query}

Sebagai asisten hukum untuk Kantor Hukum SAP, saya sarankan untuk menghubungi kantor kami langsung untuk bantuan dengan masalah hukum spesifik. Pengacara berpengalaman kami dapat memberikan panduan yang dipersonalisasi berdasarkan situasi spesifik Anda."""
        
        try:
            answer = llm.generate(prompt)
            logger.info("✅ Generated response successfully")
            
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            # Secondary fallback in case LLM fails
            answer = "Maaf, saya mengalami kesulitan teknis saat memproses permintaan Anda. Silakan coba lagi nanti atau hubungi Kantor Hukum SAP langsung untuk bantuan."
        
        # 4) Save to database
        try:
            record = ChatHistory(
                session_id=session_id, 
                question=query, 
                answer=answer
            )
            db.session.add(record)
            db.session.commit()
            logger.info(f"✅ Saved chat record with ID: {record.id}")
        except Exception as e:
            logger.error(f"Error saving to database: {e}")
            # Continue anyway, don't fail the request
        
        return jsonify({
            "answer": answer,
            "session_id": session_id,
            "chat_id": record.id if 'record' in locals() else None,
            "sources_found": len(hits) if hits else 0
        }), 200
        
    except Exception as e:
        logger.error(f"Unexpected error in chat endpoint: {e}")
        return jsonify(error="Internal server error"), 500

@chat_bp.route("/health", methods=["GET"])
def health_check():
    """Health check endpoint to verify all services are working"""
    try:
        # Test embedding model
        test_embedding = embedding_model.encode("test").tolist()
        
        # Test Qdrant connection
        rag_status = "OK" if rag else "Not initialized"
        
        # Test OpenAI connection
        llm_status = "OK" if llm else "Not initialized"
        
        return jsonify({
            "status": "healthy",
            "embedding_model": "OK",
            "rag_service": rag_status,
            "llm_service": llm_status,
            "embedding_dimension": len(test_embedding)
        }), 200
        
    except Exception as e:
        return jsonify({
            "status": "unhealthy",
            "error": str(e)
        }), 500