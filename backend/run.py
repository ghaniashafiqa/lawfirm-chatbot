# backend/run.py [PROD]

from app import create_app
from app.db import db
from alembic import command
from alembic.config import Config
import os

app = create_app()

# Only run alembic upgrade if in production (Railway)
if os.environ.get("RAILWAY_ENVIRONMENT"):
    with app.app_context():
        print("🔧 Running Alembic migrations...")
        alembic_cfg = Config("alembic.ini")
        command.upgrade(alembic_cfg, "head")

if __name__ == "__main__":
    app.run()

# backend/run.py [LOCAL]
# from app import create_app

# app = create_app()

# if __name__ == "__main__":
#     app.run(host="0.0.0.0", port=5000, debug=True)
