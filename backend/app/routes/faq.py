from flask import Blueprint, request, jsonify
from app.db import db
from app.models import FAQ
from flask_jwt_extended import jwt_required

faq_bp = Blueprint('faq', __name__, url_prefix='/faq')

@faq_bp.route('', methods=['GET'])
def list_faq():
    """Public endpoint: list all FAQ entries."""
    faqs = FAQ.query.all()
    return jsonify([
        {"id": f.id, "question": f.question, "answer": f.answer}
        for f in faqs
    ])

@faq_bp.route('', methods=['POST'])
@jwt_required()
def create_faq():
    """Admin-only: add a new FAQ."""
    data = request.get_json(force=True)
    f = FAQ(question=data['question'], answer=data['answer'])
    db.session.add(f)
    db.session.commit()
    return jsonify(msg="FAQ created", id=f.id), 201

@faq_bp.route('/<int:faq_id>', methods=['PUT'])
@jwt_required()
def update_faq(faq_id):
    data = request.get_json(force=True)
    f = FAQ.query.get_or_404(faq_id)
    f.question = data.get('question', f.question)
    f.answer   = data.get('answer',   f.answer)
    db.session.commit()
    return jsonify(msg="FAQ updated")

@faq_bp.route('/<int:faq_id>', methods=['DELETE'])
@jwt_required()
def delete_faq(faq_id):
    f = FAQ.query.get_or_404(faq_id)
    db.session.delete(f)
    db.session.commit()
    return jsonify(msg="FAQ deleted")
