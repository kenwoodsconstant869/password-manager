"""Adapter : implémentation SQLite de UserRepository."""

import sqlite3

from src.application.interfaces.user_repository import UserRepository
from src.domain.entities.user import User


class SQLiteUserRepository(UserRepository):

    def __init__(self, connection: sqlite3.Connection):
        self._conn = connection
        self._create_table_if_not_exists()

    def _create_table_if_not_exists(self) -> None:
        self._conn.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                password_hash TEXT NOT NULL,
                salt BLOB NOT NULL
            )
            """
        )
        self._conn.commit()

    def save(self, user: User) -> User:
        self._conn.execute("DELETE FROM users")
        cursor = self._conn.execute(
            "INSERT INTO users (username, password_hash, salt) VALUES (?, ?, ?)",
            (user.username, user.password_hash, user.salt),
        )
        self._conn.commit()
        user.id = cursor.lastrowid
        return user

    def get_the_user(self) -> User | None:
        row = self._conn.execute("SELECT id, username, password_hash, salt FROM users LIMIT 1").fetchone()
        if row is None:
            return None
        id_, username, password_hash, salt = row
        return User(id=id_, username=username, password_hash=password_hash, salt=salt)
