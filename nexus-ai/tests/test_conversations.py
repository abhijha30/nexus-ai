import pytest

from src.database import conversations as c
from src.database.db import init_db
from src.utils.validators import ValidationError


@pytest.fixture
def db(tmp_path):
    p = tmp_path / "t.db"
    init_db(p)
    return p


def test_create_and_get(db):
    conv = c.create_conversation("Hello", path=db)
    assert c.get_conversation(conv["id"], path=db)["title"] == "Hello"


def test_messages_roundtrip_in_order(db):
    conv = c.create_conversation("Chat", path=db)
    c.add_message(conv["id"], "user", "hi", path=db)
    c.add_message(conv["id"], "assistant", "hello", path=db)
    msgs = c.get_messages(conv["id"], path=db)
    assert [(m["role"], m["content"]) for m in msgs] == [("user", "hi"), ("assistant", "hello")]


def test_rename_and_invalid_rename(db):
    conv = c.create_conversation("Old", path=db)
    assert c.rename_conversation(conv["id"], "  New   name ", path=db) == "New name"
    with pytest.raises(ValidationError):
        c.rename_conversation(conv["id"], "   ", path=db)


def test_delete_removes_messages(db):
    conv = c.create_conversation("Gone", path=db)
    c.add_message(conv["id"], "user", "x", path=db)
    c.delete_conversation(conv["id"], path=db)
    assert c.get_conversation(conv["id"], path=db) is None
    assert c.get_messages(conv["id"], path=db) == []


def test_search_title_content_and_wildcards(db):
    a = c.create_conversation("Python tips", path=db)
    b = c.create_conversation("Cooking", path=db)
    c.add_message(b["id"], "user", "best pasta recipe", path=db)
    assert [x["id"] for x in c.list_conversations("python", path=db)] == [a["id"]]
    assert [x["id"] for x in c.list_conversations("pasta", path=db)] == [b["id"]]
    assert c.list_conversations("%", path=db) == []  # wildcard is escaped


def test_sql_injection_text_is_inert(db):
    conv = c.create_conversation("x'; DROP TABLE messages;--", path=db)
    c.add_message(conv["id"], "user", "'; DROP TABLE conversations;--", path=db)
    assert len(c.get_messages(conv["id"], path=db)) == 1


def test_updated_order_and_clear_all(db):
    a = c.create_conversation("A", path=db)
    b = c.create_conversation("B", path=db)
    c.add_message(a["id"], "user", "bump", path=db)
    assert c.list_conversations(path=db)[0]["id"] == a["id"]
    c.clear_all(path=db)
    assert c.list_conversations(path=db) == []
