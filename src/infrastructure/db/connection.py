"""Frameworks & Drivers : connexion SQLite."""

import sqlite3


def get_connection(db_path: str = "password_manager.db") -> sqlite3.Connection:
    return sqlite3.connect(db_path, check_same_thread=False)
