import os
import sqlite3
from typing import Generator

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "market_intelligence.db")

def get_db_connection() -> sqlite3.Connection:
    """Returns a thread-safe connection to the SQLite analytical database with Row factory."""
    if not os.path.exists(DB_PATH):
        raise FileNotFoundError(f"Database not found at {DB_PATH}. Run 'python main.py' to initialize.")
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def get_db() -> Generator[sqlite3.Connection, None, None]:
    """FastAPI dependency yielding a database connection."""
    conn = get_db_connection()
    try:
        yield conn
    finally:
        conn.close()
