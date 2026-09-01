"""
Run once to create all database tables:
    python scripts/init_db.py
"""

import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.db.database import engine, Base
from app.db import models  # noqa: F401  (import so tables register on Base.metadata)

if __name__ == "__main__":
    print("Creating tables...")
    Base.metadata.create_all(bind=engine)
    print("Done. Tables created:", list(Base.metadata.tables.keys()))
