from flask import Blueprint, request, jsonify
from app.db import db
from app.models import BotGreeting
from flask_jwt_extended import jwt_required

bot_bp = Blueprint('bot', __name__, url_prefix='/bot-greetings')

@bot_bp.route('', methods=['GET'])
def list_greetings():
    greetings = BotGreeting.query.order_by(BotGreeting.created_at.desc()).all()
    return jsonify([{"id": g.id, "text": g.text} for g in greetings])

@bot_bp.route('', methods=['POST'])
@jwt_required()
def create_greeting():
    data = request.get_json(force=True)
    g = BotGreeting(text=data['text'])
    db.session.add(g)
    db.session.commit()
    return jsonify(msg="Greeting created", id=g.id), 201

@bot_bp.route('/<int:greeting_id>', methods=['PUT'])
@jwt_required()
def update_greeting(greeting_id):
    g = BotGreeting.query.get_or_404(greeting_id)
    data = request.get_json(force=True)
    g.text = data.get('text', g.text)
    db.session.commit()
    return jsonify(msg="Greeting updated")

@bot_bp.route('/<int:greeting_id>', methods=['DELETE'])
@jwt_required()
def delete_greeting(greeting_id):
    g = BotGreeting.query.get_or_404(greeting_id)
    db.session.delete(g)
    db.session.commit()
    return jsonify(msg="Greeting deleted")
