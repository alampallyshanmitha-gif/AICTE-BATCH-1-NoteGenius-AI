import sqlite3
import json
import hashlib

DATABASE = "database/app.db"


# ======================
# CREATE TABLES
# ======================
def create_table():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    # USERS TABLE
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )
    """)

    # NOTES TABLE (USER-SPECIFIC)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS notes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        transcript TEXT,
        summary TEXT,
        quiz TEXT,
        flashcards TEXT,
        keywords TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(user_id) REFERENCES users(id)
    )
    """)

    conn.commit()
    conn.close()


# ======================
# PASSWORD HASHING
# ======================
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


# ======================
# REGISTER USER (SIGN UP)
# ======================
def register_user(username, email, password):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    try:
        cursor.execute("""
        INSERT INTO users (username, email, password)
        VALUES (?, ?, ?)
        """, (username, email, hash_password(password)))

        conn.commit()
        return True

    except sqlite3.IntegrityError:
        # email already exists
        return False

    finally:
        conn.close()


# ======================
# LOGIN USER
# ======================
def login_user(email, password):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("""
    SELECT id, username, password
    FROM users
    WHERE email=?
    """, (email,))

    user = cursor.fetchone()
    conn.close()

    if user:
        user_id, username, db_password = user

        if db_password == hash_password(password):
            return (user_id, username)

    return None


# ======================
# SAVE NOTE (USER-BASED)
# ======================
def save_note(user_id, transcript, summary, quiz, flashcards, keywords):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO notes (
        user_id, transcript, summary, quiz, flashcards, keywords
    )
    VALUES (?, ?, ?, ?, ?, ?)
    """, (
        user_id,
        transcript,
        summary,
        json.dumps(quiz),
        json.dumps(flashcards),
        json.dumps(keywords)
    ))

    conn.commit()
    conn.close()


# ======================
# GET NOTES (ONLY LOGGED-IN USER)
# ======================
def get_notes(user_id):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("""
    SELECT id, transcript, summary, quiz, flashcards, keywords, created_at
    FROM notes
    WHERE user_id=?
    ORDER BY id DESC
    """, (user_id,))

    notes = cursor.fetchall()
    conn.close()

    return notes


# ======================
# DELETE NOTE
# ======================
def delete_note(note_id):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("""
    DELETE FROM notes WHERE id=?
    """, (note_id,))

    conn.commit()
    conn.close()