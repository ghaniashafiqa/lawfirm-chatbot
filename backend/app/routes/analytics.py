from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required
from app.services.analytics import AnalyticsService

analytics_bp = Blueprint('analytics', __name__, url_prefix='/analytics')

@analytics_bp.route('/questions-week', methods=['GET'])
@jwt_required()
def questions_week():
    """Return number of questions asked in the past week."""
    count = AnalyticsService.questions_this_week()
    return jsonify(questions_this_week=count)

@analytics_bp.route('/users-average', methods=['GET'])
@jwt_required()
def users_average():
    """Return average distinct users per day."""
    avg = AnalyticsService.users_per_day_average()
    return jsonify(users_per_day_average=avg)

@analytics_bp.route('/docs-total', methods=['GET'])
@jwt_required()
def docs_total():
    """Return total number of documents in the vector store."""
    total = AnalyticsService.total_documents()
    return jsonify(total_documents=total)
