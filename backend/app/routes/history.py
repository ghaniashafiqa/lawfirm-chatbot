from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app.db import db
from app.models import ChatHistory, Feedback

history_bp = Blueprint('history', __name__, url_prefix='/history')

@history_bp.route('', methods=['GET'])
@jwt_required()
def list_history():
    sessions = ChatHistory.query.order_by(ChatHistory.created_at.desc()).all()
    return jsonify([
        {
            "id": h.id,
            "session_id": h.session_id,
            "question": h.question,
            "answer": h.answer,
            "created_at": h.created_at.isoformat(),
            "feedback": h.feedbacks[0].is_positive if h.feedbacks else None
        }
        for h in sessions
    ])

@history_bp.route('/<int:chat_id>/feedback', methods=['POST'])
@jwt_required()
def add_feedback(chat_id):
    """Admin: attach feedback to a chat record."""
    data = request.get_json(force=True)
    fb = Feedback(
        chat_id=chat_id,
        is_positive=bool(data.get('is_positive', True)),
        comment=data.get('comment', None)
    )
    db.session.add(fb)
    db.session.commit()
    return jsonify(msg="Feedback saved"), 201

@history_bp.route('/<int:chat_id>/feedback', methods=['GET'])
@jwt_required()
def get_feedback(chat_id):
    """Admin: fetch feedback for a given chat."""
    fbs = Feedback.query.filter_by(chat_id=chat_id).all()
    return jsonify([
        {"id": f.id, "is_positive": f.is_positive, "comment": f.comment}
        for f in fbs
    ])
