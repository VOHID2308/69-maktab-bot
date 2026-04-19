# handlers/student_handler.py
from telegram import Update
from telegram.ext import ContextTypes, CommandHandler, MessageHandler, filters
from keyboards.student_keyboard import student_menu_kb
from database import db

async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    tg = update.effective_user
    user = await db.get_user_by_tg(tg.id)
    if not user:
        await update.message.reply_text("Siz ro'yxatdan o'tmagansiz. /start bilan ro'yxatdan o'ting.")
        return
    if user.get("role") != "student":
        await update.message.reply_text("Kechirasiz, bu bo'lim faqat o'quvchilar uchun.")
        return
    name = user.get("fullname") or "O'quvchi"
    await update.message.reply_text(f"Salom, {name}!\nQuyidagilardan birini tanlang:", reply_markup=student_menu_kb())

async def show_class(update: Update, context: ContextTypes.DEFAULT_TYPE):
    tg = update.effective_user
    user = await db.get_user_by_tg(tg.id)
    if not user or not user.get("class_name"):
        await update.message.reply_text("Sinf ma'lum emas. /start bilan qayta ro'yxatdan o'ting.")
        return
    class_name = user.get("class_name")
    students = await db.get_students_in_class(class_name)
    lines = [f"- {s.get('fullname') or s.get('telegram_username') or 'NoName'}" for s in students]
    await update.message.reply_text(f"Sinf: {class_name}\nA'zolari:\n" + "\n".join(lines))

def get_handlers():
    return [
        CommandHandler("menu", menu),
        CommandHandler("sinf", show_class),
        MessageHandler(filters.Regex(r"^/sinf$"), show_class),
    ]
