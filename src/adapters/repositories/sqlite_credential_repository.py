"""Adapter : implémentation SQLite de CredentialRepository."""

import sqlite3
from datetime import datetime

from src.application.interfaces.credential_repository import CredentialRepository
from src.domain.entities.credential import Credential


class SQLiteCredentialRepository(CredentialRepository):

    def __init__(self, connection: sqlite3.Connection):
        self._conn = connection
        self._create_table_if_not_exists()

    def _create_table_if_not_exists(self) -> None:
        self._conn.execute(
            """
            CREATE TABLE IF NOT EXISTS credentials (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                service TEXT NOT NULL,
                username TEXT NOT NULL,
                password TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
            """
        )
        self._conn.commit()

    def add(self, credential: Credential) -> Credential:
        cursor = self._conn.execute(
            "INSERT INTO credentials (service, username, password, created_at) VALUES (?, ?, ?, ?)",
            (credential.service, credential.username, credential.password, credential.created_at.isoformat()),
        )
        self._conn.commit()
        credential.id = cursor.lastrowid
        return credential

    def close(self) -> None:
        self._conn.close()

    def get_by_id(self, credential_id: int) -> Credential | None:
        row = self._conn.execute(
            "SELECT id, service, username, password, created_at FROM credentials WHERE id = ?",
            (credential_id,),
        ).fetchone()
        return self._row_to_entity(row) if row else None

    def get_all(self) -> list[Credential]:
        rows = self._conn.execute(
            "SELECT id, service, username, password, created_at FROM credentials"
        ).fetchall()
        return [self._row_to_entity(row) for row in rows]

    def update(self, credential: Credential) -> None:
        self._conn.execute(
            "UPDATE credentials SET service = ?, username = ?, password = ? WHERE id = ?",
            (credential.service, credential.username, credential.password, credential.id),
        )
        self._conn.commit()

    def delete(self, credential_id: int) -> None:
        self._conn.execute("DELETE FROM credentials WHERE id = ?", (credential_id,))
        self._conn.commit()

    @staticmethod
    def _row_to_entity(row: tuple) -> Credential:
        id_, service, username, password, created_at = row
        return Credential(id=id_, service=service, username=username, password=password,
                           created_at=datetime.fromisoformat(created_at))
