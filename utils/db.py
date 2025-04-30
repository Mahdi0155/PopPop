import sqlite3
from datetime import datetime, timedelta

conn = sqlite3.connect("data/database.db", check_same_thread=False)
cur = conn.cursor()

def init_db():
    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY,
        join_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS files (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        file_id TEXT,
        type TEXT,
        user_id INTEGER,
        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    conn.commit()

def add_user(user_id: int):
    cur.execute("INSERT OR IGNORE INTO users (user_id) VALUES (?)", (user_id,))
    conn.commit()

def get_stats():
    now = datetime.now()
    cur.execute("SELECT COUNT(*) FROM users")
    total_users = cur.fetchone()[0]

    def count_from(delta):
        time = now - delta
        cur.execute("SELECT COUNT(*) FROM users WHERE join_date >= ?", (time,))
        return cur.fetchone()[0]

    def count_files():
        cur.execute("SELECT COUNT(*) FROM files")
        return cur.fetchone()[0]

    return {
        'total_users': total_users,
        'hour_users': count_from(timedelta(hours=1)),
        'day_users': count_from(timedelta(days=1)),
        'week_users': count_from(timedelta(weeks=1)),
        'month_users': count_from(timedelta(days=30)),
        'total_files': count_files()
    }

def log_file(file_id: str, file_type: str, user_id: int) -> int:
    cur.execute("INSERT INTO files (file_id, type, user_id) VALUES (?, ?, ?)", (file_id, file_type, user_id))
    conn.commit()
    return cur.lastrowid  # برمی‌گرداند ID دیتابیس برای استفاده در لینک مستقیم

def get_file_by_id(file_db_id: int):
    cur.execute("SELECT file_id, type FROM files WHERE id = ?", (file_db_id,))
    return cur.fetchone()

def get_file_by_id(file_db_id: int):
    cur.execute("SELECT file_id, type FROM files WHERE id = ?", (file_db_id,))
    row = cur.fetchone()
    if row:
        return {"file_id": row[0], "type": row[1]}
    return None

def get_file_by_id(file_db_id: str):
    cur.execute("SELECT file_id FROM files WHERE id = ?", (file_db_id,))
    row = cur.fetchone()
    if row:
        return {"file_id": row[0]}
    return None
