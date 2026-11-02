
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "data" / "skillscope.db"


def get_connection():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")

    return connection


def initialize_chat_storage():
    with get_connection() as connection:
        connection.executescript(
            """
            CREATE TABLE IF NOT EXISTS conversations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL DEFAULT 'New conversation',
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                conversation_id INTEGER NOT NULL,
                role TEXT NOT NULL CHECK (role IN ('user', 'assistant')),
                content TEXT NOT NULL,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (conversation_id)
                    REFERENCES conversations(id)
                    ON DELETE CASCADE
            );
            """
        )

def create_conversation(title="New conversation"):
    with get_connection() as connection:
        cursor = connection.execute(
            "INSERT INTO conversations (title) VALUES (?)",
            (title,),
        )
        return cursor.lastrowid


def get_conversations():
    with get_connection() as connection:
        rows = connection.execute(
            """
            SELECT id, title, created_at, updated_at
            FROM conversations
            ORDER BY updated_at DESC, id DESC
            """
        ).fetchall()

        return [dict(row) for row in rows]


def save_message(conversation_id, role, content):
    if role not in ("user", "assistant"):
        raise ValueError("Role must be 'user' or 'assistant'.")

    with get_connection() as connection:
        connection.execute(
            """
            INSERT INTO messages (conversation_id, role, content)
            VALUES (?, ?, ?)
            """,
            (conversation_id, role, content),
        )

        connection.execute(
            """
            UPDATE conversations
            SET updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
            """,
            (conversation_id,),
        )


def get_messages(conversation_id):
    with get_connection() as connection:
        rows = connection.execute(
            """
            SELECT id, conversation_id, role, content, created_at
            FROM messages
            WHERE conversation_id = ?
            ORDER BY id ASC
            """,
            (conversation_id,),
        ).fetchall()

        return [dict(row) for row in rows]


def rename_conversation(conversation_id, title):
    title = title.strip()

    if not title:
        raise ValueError("Conversation title cannot be empty.")

    with get_connection() as connection:
        connection.execute(
            """
            UPDATE conversations
            SET title = ?, updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
            """,
            (title, conversation_id),
        )


def delete_conversation(conversation_id):
    with get_connection() as connection:
        connection.execute(
            "DELETE FROM conversations WHERE id = ?",
            (conversation_id,),
        )