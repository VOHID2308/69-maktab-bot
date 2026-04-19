# database/db.py
import sqlite3
import asyncio
from config.settings import DB_PATH

def create_tables():
    """Bazani va kerakli jadvallarni yaratadi."""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # Users jadvali
    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        tg_id INTEGER UNIQUE,
        fullname TEXT,
        role TEXT,
        class_name TEXT,
        telegram_username TEXT
    )
    """)

    # Classes jadvali
    cur.execute("""
    CREATE TABLE IF NOT EXISTS classes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE
    )
    """)

    conn.commit()
    conn.close()


async def get_classes():
    """Barcha sinflarni qaytaradi."""
    def query():
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        cur.execute("SELECT name FROM classes ORDER BY name")
        rows = [r[0] for r in cur.fetchall()]
        conn.close()
        return rows
    return await asyncio.to_thread(query)


async def add_class(name: str):
    """Yangi sinfni qo'shadi (agar mavjud bo'lmasa)."""
    def insert():
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        cur.execute("INSERT OR IGNORE INTO classes (name) VALUES (?)", (name,))
        conn.commit()
        conn.close()
    await asyncio.to_thread(insert)


async def create_or_update_user(tg_id: int, role: str, telegram_username: str = None):
    """Yangi foydalanuvchini yaratadi yoki yangilaydi."""
    def create_or_update_user_sync(tg_id, role, telegram_username):
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        cur.execute("SELECT id FROM users WHERE tg_id = ?", (tg_id,))
        row = cur.fetchone()
        if row:
            cur.execute("UPDATE users SET role = ?, telegram_username = ? WHERE tg_id = ?",
                        (role, telegram_username, tg_id))
        else:
            cur.execute("INSERT INTO users (tg_id, role, telegram_username) VALUES (?, ?, ?)",
                        (tg_id, role, telegram_username))
        conn.commit()
        conn.close()
    await asyncio.to_thread(create_or_update_user_sync, tg_id, role, telegram_username)


async def set_user_class_fullname(tg_id: int, class_name: str, fullname: str):
    """O‘quvchining sinfini va to‘liq ismini saqlaydi."""
    def update_user():
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        cur.execute("UPDATE users SET class_name = ?, fullname = ? WHERE tg_id = ?", (class_name, fullname, tg_id))
        conn.commit()
        conn.close()
    await asyncio.to_thread(update_user)


async def get_students_in_class(class_name: str):
    """Berilgan sinfdagi barcha o‘quvchilarni qaytaradi."""
    def query():
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        cur.execute("SELECT fullname, telegram_username FROM users WHERE class_name = ? AND role = 'student'", (class_name,))
        rows = [{"fullname": r[0], "telegram_username": r[1]} for r in cur.fetchall()]
        conn.close()
        return rows
    return await asyncio.to_thread(query)


# ✅ dastur yuklanganda avtomatik jadval yaratish
create_tables()
