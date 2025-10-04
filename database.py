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

    cur.execute("""
            CREATE TABLE IF NOT EXISTS uploaded_files (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                application_name TEXT NOT NULL,
                filename TEXT NOT NULL,
                content_type TEXT,
                file_data BLOB,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
                """)
    
    connection.commit()


def insert_file(application_name:str, file_name:str, content_type:str, file_bytes:bytes):
    connection = get_connection()
    cur = connection.cursor()

    cur.execute("""
            INSERT INTO uploaded_files (application_name,filename,content_type,file_data)
                VALUES (?,?,?,?)
                """,(application_name,file_name,content_type,file_bytes))
    
    connection.commit()

def close_connection():
    global conn
    
    if conn is not None:
        conn.close()
        conn = None
