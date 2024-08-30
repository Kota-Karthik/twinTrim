# twinTrim/db.py

import sqlite3
import click
import os

DATABASE = 'files.db'  

def create_tables():
    """Create necessary tables in the SQLite database."""
    try:
        with sqlite3.connect(DATABASE) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS files (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    file_path TEXT UNIQUE,
                    file_hash TEXT
                )
            """)
            cursor.execute("CREATE INDEX IF NOT EXISTS file_hash_index ON files(file_hash)")
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS duplicates (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    original_id INTEGER,
                    duplicate_id INTEGER,
                    FOREIGN KEY (original_id) REFERENCES files(id),
                    FOREIGN KEY (duplicate_id) REFERENCES files(id)
                )
            """)
            cursor.execute("CREATE INDEX IF NOT EXISTS original_id_index ON duplicates(original_id)")

            cursor.execute("CREATE INDEX IF NOT EXISTS duplicate_id_index ON duplicates(duplicate_id)")

            conn.commit()
    except sqlite3.Error as error:
        print(f"Database Error: {error}")

def insert_file(file_path, file_hash):
    """Insert a file record into the database."""
    try:
        with sqlite3.connect(DATABASE) as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT OR IGNORE INTO files (file_path, file_hash) VALUES (?, ?)", (file_path, file_hash))
            conn.commit()
    except sqlite3.Error as error:
        print(f"Database Error: {error}")

def insert_files(file_data):
    """
    Insert multiple file records into the database at once.
    
    Args:
    file_data (list of tuples): Each tuple contains (file_path, file_hash).
    """
    try:
        with sqlite3.connect(DATABASE) as conn:
            cursor = conn.cursor()
            # Use executemany for batch insertion
            cursor.executemany(
                "INSERT OR IGNORE INTO files (file_path, file_hash) VALUES (?, ?)", 
                file_data
            )
            conn.commit()
    except sqlite3.Error as error:
        print(f"Database Error: {error}")

def insert_duplicates(duplicates_data):
    """
    Insert multiple duplicate records into the database at once.
    
    Args:
    duplicates_data (list of tuples): Each tuple contains (original_path, duplicate_path).
    """
    try:
        with sqlite3.connect(DATABASE) as conn:
            cursor = conn.cursor()
            # Prepare the insert statement for batch processing
            cursor.executemany("""
                INSERT INTO duplicates (original_id, duplicate_id) 
                VALUES (
                    (SELECT id FROM files WHERE file_path = ? LIMIT 1), 
                    (SELECT id FROM files WHERE file_path = ? LIMIT 1)
                )
            """, duplicates_data)
            conn.commit()
    except sqlite3.Error as error:
        print(f"Database Error: {error}")

def query_duplicates():
    """Query and return all duplicates from the database."""
    try:
        with sqlite3.connect(DATABASE) as conn:
            cursor = conn.cursor()
            # SELECT (SELECT file_path FROM files WHERE id = original_id), (SELECT file_path FROM files WHERE id=duplicate_id) FROM duplicates;
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

def drop_all_tables():
    """Drop all tables from the database."""
    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()

        # Enable writable schema to allow dropping tables
        # cursor.execute("PRAGMA writable_schema = 1")
        # cursor.execute("PRAGMA foreign_keys = OFF")

        # # Get the list of tables
        # cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        # tables = cursor.fetchall()

        tables = ["duplicates", "files"] # remove duplicates first as it has some foreign key dependency on files

        # Drop each table
        for table in tables:
            table_name = table[0]
            cursor.execute(f"TRUNCATE TABLE IF EXISTS {table_name}")
            click.echo(click.style(f"Truncate table: {table_name}", fg='green'))

        # Re-enable foreign key checks
        # cursor.execute("PRAGMA foreign_keys = ON")

        conn.commit()
        conn.close()
        click.echo(click.style("All tables dropped from the database.", fg='green'))
    except Exception as e:
        click.echo(click.style(f"Error dropping tables from database: {e}", fg='red'))


def recreate_database():
    """Delete and recreate the database."""
    try:
        if os.path.exists(DATABASE):
            os.remove(DATABASE)
            click.echo(click.style("Old database removed.", fg='green'))

        # Create a new database and initialize schema
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        # Initialize schema (create tables, etc.)
        # Example: cursor.execute("CREATE TABLE files (path TEXT PRIMARY KEY)")
        conn.commit()
        conn.close()
        click.echo(click.style("New database created.", fg='green'))
    except Exception as e:
        click.echo(click.style(f"Error recreating the database: {e}", fg='red'))
