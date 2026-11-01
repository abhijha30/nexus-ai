import sqlite3

import pytest

from src.database.db import DatabaseError, connect, init_db


def test_init_creates_tables(tmp_path):
    path = tmp_path / "t.db"
    init_db(path)
    init_db(path)  # idempotent
    names = {r[0] for r in sqlite3.connect(path).execute("SELECT name FROM sqlite_master WHERE type='table'")}
    assert {"conversations", "messages"} <= names


def test_unopenable_path_raises_database_error(tmp_path):
    blocker = tmp_path / "file"
    blocker.write_text("x")
    with pytest.raises(DatabaseError):
        with connect(blocker / "sub" / "t.db"):
            pass
