from flask import Flask
from flask_migrate import Migrate
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from .config import Config
from .db import db
from .models import Admin, ChatHistory, Feedback, FAQ, Setting

# import routes so they register
from .routes.auth import auth_bp
from .routes.chat import chat_bp
from .routes.kb import kb_bp
from .routes.faq import faq_bp
from .routes.history import history_bp
from .routes.admin import admin_bp
from .routes.analytics import analytics_bp

jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    Migrate(app, db)
    CORS(app)
    jwt.init_app(app)

    # register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(chat_bp)
    app.register_blueprint(kb_bp)
    app.register_blueprint(faq_bp)
    app.register_blueprint(history_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(analytics_bp)

    return app