import os 
from datetime import timedelta
from dotenv import load_dotenv

print("✅ DATABASE_URL from env:", os.getenv("DATABASE_URL"))

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '..', '.env'))

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv("JWT_SECRET")
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=2)
    QDRANT_URL = os.getenv("QDRANT_URL")
    QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
    COLLECTION_NAME = os.getenv("COLLECTION_NAME", "gebukmantan_posts_recursive")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")