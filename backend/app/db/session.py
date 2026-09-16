import os
import sqlite3
from contextlib import contextmanager
from app.core.config import settings

def init_db_pragmas():
    """Initialize SQLite PRAGMAs for concurrency and performance."""
    try:
        conn = sqlite3.connect(settings.DB_PATH)
        conn.execute("PRAGMA journal_mode = WAL;")
        conn.execute("PRAGMA synchronous = NORMAL;")
        conn.execute("PRAGMA busy_timeout = 5000;")
        conn.close()
    except Exception as e:
        print(f"Warning: Could not configure WAL mode: {e}")

from pathlib import Path

@contextmanager
def get_db(read_only: bool = True):
    """
    Yields a SQLite connection.
    Defaults to read_only mode for high concurrency read operations.
    """
    if read_only and os.path.exists(settings.DB_PATH):
        db_uri = f"{Path(settings.DB_PATH).resolve().as_uri()}?mode=ro"
        conn = sqlite3.connect(db_uri, uri=True, timeout=5.0)
    else:
        conn = sqlite3.connect(settings.DB_PATH, timeout=5.0)


    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA busy_timeout = 5000;")
    try:
        yield conn
    finally:
        conn.close()

