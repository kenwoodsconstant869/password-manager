"""Frameworks & Drivers : connexion SQLite."""

import os
import sqlite3


def get_connection(db_path: str | None = None) -> sqlite3.Connection:
    resolved_path = db_path or os.environ.get("PASSWORD_MANAGER_DB_PATH", "password_manager.db")
    directory = os.path.dirname(resolved_path)
    if directory:
        os.makedirs(directory, exist_ok=True)
    connection = sqlite3.connect(resolved_path, check_same_thread=False)
    connection.row_factory = sqlite3.Row
    return connection
