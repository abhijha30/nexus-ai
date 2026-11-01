"""SQLite connection + schema. Swap this module (and conversations.py) to move to PostgreSQL later."""
import logging
import sqlite3
from contextlib import contextmanager
from pathlib import Path

from src.config.settings import DB_PATH

log = logging.getLogger(__name__)


class DatabaseError(Exception):
    """Storage failed. Details go to the log, not the UI."""


SCHEMA = """
CREATE TABLE IF NOT EXISTS conversations (
    id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    conversation_id TEXT NOT NULL REFERENCES conversations(id) ON DELETE CASCADE,
    role TEXT NOT NULL CHECK (role IN ('user', 'assistant')),
    content TEXT NOT NULL,
    created_at TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_messages_conv ON messages(conversation_id, id);
CREATE INDEX IF NOT EXISTS idx_conv_updated ON conversations(updated_at DESC);
"""


@contextmanager
def connect(path=None):
    path = Path(path or DB_PATH)
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        conn = sqlite3.connect(path)
    except (sqlite3.Error, OSError) as exc:
        log.error("database open failed: %s", type(exc).__name__)
        raise DatabaseError("Could not open the chat database.") from exc
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    try:
        yield conn
        conn.commit()
    except sqlite3.Error as exc:
        conn.rollback()
        log.error("database error: %s", exc)
        raise DatabaseError("Something went wrong saving your chats.") from exc
    finally:
        conn.close()


def init_db(path=None) -> None:
    with connect(path) as conn:
        conn.executescript(SCHEMA)
