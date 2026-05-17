import sqlite3

DB_NAME = "database/helpdesk.db"

def connect_db():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def create_tables():

    conn = connect_db()
    cursor = conn.cursor()

    # USERS TABLE
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        email TEXT UNIQUE,
        password TEXT,
        role TEXT
    )
    """)

    # TICKETS TABLE
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tickets (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        sender_email TEXT,
        subject TEXT,
        message TEXT,
        priority TEXT,
        status TEXT,
        assigned_to INTEGER,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # REPLIES TABLE
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS replies (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ticket_id INTEGER,
        sender TEXT,
        message TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()
    conn.close()

create_tables()

