"""Conversation + message storage. All SQL is parameterized."""
import uuid
from datetime import datetime, timezone

from src.database.db import connect
from src.utils.validators import validate_title


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _like(q: str) -> str:
    return "%" + q.replace("\\", "\\\\").replace("%", "\\%").replace("_", "\\_") + "%"


def create_conversation(title: str = "New chat", path=None) -> dict:
    title = validate_title(title)
    conv = {"id": uuid.uuid4().hex, "title": title, "created_at": _now(), "updated_at": _now()}
    with connect(path) as conn:
        conn.execute(
            "INSERT INTO conversations (id, title, created_at, updated_at) VALUES (?, ?, ?, ?)",
            (conv["id"], conv["title"], conv["created_at"], conv["updated_at"]),
        )
    return conv


def get_conversation(conv_id: str, path=None) -> dict | None:
    with connect(path) as conn:
        row = conn.execute("SELECT * FROM conversations WHERE id = ?", (conv_id,)).fetchone()
    return dict(row) if row else None


def list_conversations(query: str = "", limit: int = 100, path=None) -> list[dict]:
    query = (query or "").strip()
    with connect(path) as conn:
        if query:
            pat = _like(query)
            rows = conn.execute(
                "SELECT * FROM conversations WHERE title LIKE ? ESCAPE '\\' OR id IN "
                "(SELECT conversation_id FROM messages WHERE content LIKE ? ESCAPE '\\') "
                "ORDER BY updated_at DESC LIMIT ?",
                (pat, pat, limit),
            ).fetchall()
        else:
            rows = conn.execute(
                "SELECT * FROM conversations ORDER BY updated_at DESC LIMIT ?", (limit,)
            ).fetchall()
    return [dict(r) for r in rows]


def rename_conversation(conv_id: str, title: str, path=None) -> str:
    title = validate_title(title)
    with connect(path) as conn:
        conn.execute(
            "UPDATE conversations SET title = ?, updated_at = ? WHERE id = ?",
            (title, _now(), conv_id),
        )
    return title


def delete_conversation(conv_id: str, path=None) -> None:
    with connect(path) as conn:
        conn.execute("DELETE FROM conversations WHERE id = ?", (conv_id,))


def clear_all(path=None) -> None:
    with connect(path) as conn:
        conn.execute("DELETE FROM conversations")


def add_message(conv_id: str, role: str, content: str, path=None) -> dict:
    now = _now()
    with connect(path) as conn:
        conn.execute(
            "INSERT INTO messages (conversation_id, role, content, created_at) VALUES (?, ?, ?, ?)",
            (conv_id, role, content, now),
        )
        conn.execute("UPDATE conversations SET updated_at = ? WHERE id = ?", (now, conv_id))
    return {"role": role, "content": content, "created_at": now}


def get_messages(conv_id: str, path=None) -> list[dict]:
    with connect(path) as conn:
        rows = conn.execute(
            "SELECT role, content, created_at FROM messages WHERE conversation_id = ? ORDER BY id",
            (conv_id,),
        ).fetchall()
    return [dict(r) for r in rows]
