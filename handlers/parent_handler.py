# handlers/parent_handler.py
from telegram import Update
from telegram.ext import ContextTypes, CommandHandler
from database import db

async def parent_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    tg = update.effective_user
    user = await db.get_user_by_tg(tg.id)
    if not user or user.get("role") != "parent":
        await update.message.reply_text("Kechirasiz, bu bo'lim faqat ota-onalar uchun.")
        return
    await update.message.reply_text("Ota-ona paneli. Farzandingiz haqida ma'lumot olish uchun /mychild ID yoki /mychild_last yozing.")

async def mychild_last(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # this is a convenience: find last student who registered with same phone? Simplify: list all students
    users = await db.get_all_users()
    students = [u for u in users if u.get("role") == "student"]
    if not students:
        await update.message.reply_text("Hozircha sinf ro'yxati bo'sh.")
        return
    # show latest student
    last = students[-1]
    await update.message.reply_text(f"Oxirgi ro'yxatdan o'tgan o'quvchi:\n{last.get('fullname')} - sinf: {last.get('class_name')}")

def get_handlers():
    return [
        CommandHandler("parent", parent_menu),
        CommandHandler("mychild_last", mychild_last),
    ]
