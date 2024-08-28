# twinTrim/db.py

import sqlite3

def create_tables():
    """Create necessary tables in the SQLite database."""
    try:
        with sqlite3.connect("files.db") as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS files (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    file_path TEXT UNIQUE,
                    file_hash TEXT
                )
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS duplicates (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    original_id INTEGER,
                    duplicate_id INTEGER,
                    FOREIGN KEY (original_id) REFERENCES files(id),
                    FOREIGN KEY (duplicate_id) REFERENCES files(id)
                )
            """)
            conn.commit()
    except sqlite3.Error as error:
        print(f"Database Error: {error}")

def insert_file(file_path, file_hash):
    """Insert a file record into the database."""
    try:
        with sqlite3.connect("files.db") as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT OR IGNORE INTO files (file_path, file_hash) VALUES (?, ?)", (file_path, file_hash))
            conn.commit()
    except sqlite3.Error as error:
        print(f"Database Error: {error}")

def insert_duplicate(original_path, duplicate_path):
    """Insert a duplicate record into the database."""
    try:
        with sqlite3.connect("files.db") as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM files WHERE file_path = ?", (original_path,))
            original_id = cursor.fetchone()[0]
            cursor.execute("SELECT id FROM files WHERE file_path = ?", (duplicate_path,))
            duplicate_id = cursor.fetchone()[0]
            cursor.execute("INSERT INTO duplicates (original_id, duplicate_id) VALUES (?, ?)", (original_id, duplicate_id))
            conn.commit()
    except sqlite3.Error as error:
        print(f"Database Error: {error}")

def query_duplicates():
    """Query and return all duplicates from the database."""
    try:
        with sqlite3.connect("files.db") as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT f1.file_path AS original, f2.file_path AS duplicate
                FROM duplicates d
                JOIN files f1 ON d.original_id = f1.id
                JOIN files f2 ON d.duplicate_id = f2.id
            """)
            return cursor.fetchall()
    except sqlite3.Error as error:
        print(f"Database Error: {error}")
        return []
