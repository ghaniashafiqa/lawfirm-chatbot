from .db import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

class Admin(db.Model):
    __tablename__ = "admins"
    id           = db.Column(db.Integer, primary_key=True)
    username     = db.Column(db.String(50), unique=True, nullable=False)
    email        = db.Column(db.String(100), unique=True, nullable=False)
    password_h   = db.Column(db.Text, nullable=False)
    role         = db.Column(db.String(20), default="admin")
    created_at   = db.Column(db.DateTime, server_default=db.func.now())

    sessions     = db.relationship("Session", backref="admin", lazy=True)

    def set_password(self, pw):
        self.password_h = generate_password_hash(pw)

    def check_password(self, pw):
        return check_password_hash(self.password_h, pw)


class Session(db.Model):
    __tablename__ = "sessions"
    id          = db.Column(db.Integer, primary_key=True)
    admin_id    = db.Column(db.Integer, db.ForeignKey("admins.id"), nullable=False)
    ip          = db.Column(db.String(50))
    device      = db.Column(db.String(100))
    location    = db.Column(db.String(100))
    user_agent  = db.Column(db.Text)
    current     = db.Column(db.Boolean, default=True)
    last_active = db.Column(db.DateTime, default=datetime.utcnow)
    

class ChatHistory(db.Model):
    __tablename__ = "chat_history"
    id         = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.String(36), nullable=False)
    question   = db.Column(db.Text, nullable=False)
    answer     = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    feedbacks = db.relationship("Feedback", backref="chat", lazy=True)


class Feedback(db.Model):
    __tablename__ = "feedback"
    id         = db.Column(db.Integer, primary_key=True)
    chat_id    = db.Column(db.Integer, db.ForeignKey("chat_history.id"), nullable=False)
    is_positive = db.Column(db.Boolean, nullable=False)
    comment    = db.Column(db.Text)
    created_at = db.Column(db.DateTime, server_default=db.func.now())


class FAQ(db.Model):
    __tablename__ = "faq"
    id         = db.Column(db.Integer, primary_key=True)
    question   = db.Column(db.Text, nullable=False)
    answer     = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())


class Setting(db.Model):
    __tablename__ = "settings"
    id         = db.Column(db.Integer, primary_key=True)
    key        = db.Column(db.String(50), unique=True, nullable=False)
    value      = db.Column(db.Text, nullable=False)
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())
