import sqlite3
import os
from werkzeug.security import generate_password_hash

DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'expense_tracker.db')


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    conn = get_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id            INTEGER PRIMARY KEY AUTOINCREMENT,
            name          TEXT    NOT NULL,
            email         TEXT    UNIQUE NOT NULL,
            password_hash TEXT    NOT NULL,
            created_at    TEXT    DEFAULT (datetime('now'))
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id     INTEGER NOT NULL REFERENCES users(id),
            amount      REAL    NOT NULL,
            category    TEXT    NOT NULL,
            date        TEXT    NOT NULL,
            description TEXT,
            created_at  TEXT    DEFAULT (datetime('now'))
        )
    """)
    conn.commit()
    conn.close()


def seed_db():
    conn = get_db()
    if conn.execute("SELECT COUNT(*) FROM users").fetchone()[0] > 0:
        conn.close()
        return

    conn.execute(
        "INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)",
        ("Demo User", "demo@spendly.com", generate_password_hash("demo123"))
    )
    user_id = conn.execute(
        "SELECT id FROM users WHERE email = ?", ("demo@spendly.com",)
    ).fetchone()["id"]

    expenses = [
        (user_id, 12.50,  "Food",          "2026-05-01", "Lunch at the campus café"),
        (user_id, 3.20,   "Transport",     "2026-05-03", "Bus fare to downtown"),
        (user_id, 85.00,  "Bills",         "2026-05-05", "Monthly internet bill"),
        (user_id, 45.00,  "Health",        "2026-05-08", "Pharmacy — vitamins"),
        (user_id, 18.99,  "Entertainment", "2026-05-12", "Movie ticket"),
        (user_id, 62.40,  "Shopping",      "2026-05-15", "New running shoes"),
        (user_id, 9.80,   "Food",          "2026-05-18", "Grocery run — snacks"),
        (user_id, 5.00,   "Other",         "2026-05-22", "Donation to street musician"),
    ]
    conn.executemany(
        "INSERT INTO expenses (user_id, amount, category, date, description) VALUES (?, ?, ?, ?, ?)",
        expenses
    )
    conn.commit()
    conn.close()


def create_user(name, email, password):
    conn = get_db()
    conn.execute(
        "INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)",
        (name, email, generate_password_hash(password))
    )
    conn.commit()
    conn.close()


def get_user_by_email(email):
    conn = get_db()
    user = conn.execute(
        "SELECT * FROM users WHERE email = ?", (email,)
    ).fetchone()
    conn.close()
    return user
