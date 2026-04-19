import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID", "0"))
DB_PATH = os.getenv("DB_PATH", "database/school.db")

STUDENT_PASSWORD = os.getenv("STUDENT_PASSWORD", "1111")
TEACHER_PASSWORD = os.getenv("TEACHER_PASSWORD", "2222")
PARENT_PASSWORD = os.getenv("PARENT_PASSWORD", "3333")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "4444")

# Intro videolar (ixtiyoriy)
INTRO_VIDEOS = {
    "student": "videos/student_intro.mp4",
    "teacher": "videos/teacher_intro.mp4",
    "parent": "videos/parent_intro.mp4",
    "admin": "videos/admin_intro.mp4",
}

TOKEN = BOT_TOKEN
