import sqlite3
from typing import Optional

DB_NAME = "files.db"

conn: Optional[sqlite3.Connection] = None


def get_connection():
    global conn

    if conn is None:
        conn = sqlite3.connect(DB_NAME, check_same_thread=False)
        conn.row_factory = sqlite3.Row

    return conn


def init_db():
    connection = get_connection()
    cur = connection.cursor()

    cur.execute(
        """
            CREATE TABLE IF NOT EXISTS uploaded_files (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                application_name TEXT NOT NULL,
                filename TEXT NOT NULL,
                content_type TEXT,
                file_data BLOB,
                version INTEGER NOT NULL DEFAULT 1,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
    )

    connection.commit()


def insert_file(
    application_name: str, file_name: str, content_type: str, file_bytes: bytes
):
    connection = get_connection()
    cur = connection.cursor()

    cur.execute(
        """
        SELECT MAX(version) FROM uploaded_files WHERE application_name = ?
    """,
        (application_name,),
    )
    max_version = cur.fetchone()[0]
    new_version = max_version + 1 if max_version else 1

    cur.execute(
        """
            INSERT INTO uploaded_files (application_name, filename, content_type, file_data, version)
            VALUES (?, ?, ?, ?, ?)
            """,
        (application_name, file_name, content_type, file_bytes, new_version),
    )

    connection.commit()


def get_latest_file(application_name: str):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT * FROM uploaded_files
        WHERE application_name = ?
        ORDER BY version DESC, updated_at DESC
        LIMIT 1
    """,
        (application_name,),
    )

    latest_file = cursor.fetchone()

    return latest_file


def get_spec_by_version_and_application(application_name: str, version_id: int):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
                    SELECT * FROM uploaded_files
                    WHERE application_name=? AND
                    version=?
                   """,
        (application_name, version_id),
    )

    result = cursor.fetchone()

    return result


def close_connection():
    global conn

    if conn is not None:
        conn.close()
        conn = None
