# handlers/teacher_handler.py
from telegram import Update
from telegram.ext import ContextTypes, CommandHandler
from database import db

async def teacher_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    tg = update.effective_user
    user = await db.get_user_by_tg(tg.id)
    if not user or user.get("role") != "teacher":
        await update.message.reply_text("Kechirasiz, bu bo'lim faqat o'qituvchilar uchun.")
        return
    await update.message.reply_text("O'qituvchi paneli. Hozircha quyidagi buyruqlar mavjud:\n/list_students - sinfni ko'rsatish")

async def list_students(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # for simplicity, teacher provides class name as arg: /list_students 11-A
    args = context.args
    if not args:
        await update.message.reply_text("Iltimos sinf nomini yozing: /list_students 11-A")
        return
    class_name = args[0]
    students = await db.get_students_in_class(class_name)
    if not students:
        await update.message.reply_text(f"{class_name} sinfida o'quvchilar topilmadi.")
        return
    lines = [f"- {s.get('fullname') or s.get('telegram_username')}" for s in students]
    await update.message.reply_text(f"Sinf: {class_name}\n" + "\n".join(lines))

def get_handlers():
    return [
        CommandHandler("teacher", teacher_menu),
        CommandHandler("list_students", list_students),
    ]
