from datetime import datetime, timedelta
from sqlalchemy import func
from app.db import db
from app.models import ChatHistory
from qdrant_client import QdrantClient
from app.config import Config

class AnalyticsService:
    @staticmethod
    def questions_this_week():
        """Count all chats in the last 7 days."""
        week_ago = datetime.utcnow() - timedelta(days=7)
        return ChatHistory.query.filter(ChatHistory.created_at >= week_ago).count()

    @staticmethod
    def users_per_day_average():
        """Average number of distinct sessions per day over the last 7 days."""
        week_ago = datetime.utcnow() - timedelta(days=7)
        rows = (
            db.session.query(
                func.date(ChatHistory.created_at).label("day"),
                func.count(func.distinct(ChatHistory.session_id)).label("users"),
            )
            .filter(ChatHistory.created_at >= week_ago)
            .group_by("day")
            .all()
        )
        if not rows:
            return 0
        avg = sum(r.users for r in rows) / len(rows)
        return round(avg, 2)

    @staticmethod
    def total_documents():
        """Return total number of points in the Qdrant collection."""
        client = QdrantClient(url=Config.QDRANT_URL, api_key=Config.QDRANT_API_KEY)
        info = client.get_collections().collections
        for col in info:
            if col.name == "law_docs":
                # Newer Qdrant Python returns col.vectors_count
                return getattr(col, "vectors_count", getattr(col, "points_count", 0))
        return 0
