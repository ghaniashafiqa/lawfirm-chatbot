from app import create_app
from app.db import db
from alembic.config import Config
from alembic import command
import os

app = create_app()

with app.app_context():
    print("✅ App context started")
    alembic_cfg = Config("alembic.ini")
    command.upgrade(alembic_cfg, "head")
    print("✅ Migration complete")
