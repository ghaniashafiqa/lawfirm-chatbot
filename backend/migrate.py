from app import create_app
from alembic import command
from alembic.config import Config
import os

app = create_app()

with app.app_context():
    print("🔧 Running Alembic migrations...")
    cfg_path = os.path.join(os.path.dirname(__file__), 'alembic.ini')
    print("📄 Alembic config path:", cfg_path)
    alembic_cfg = Config(cfg_path)
    command.upgrade(alembic_cfg, "head")
