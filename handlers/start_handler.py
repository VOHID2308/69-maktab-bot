# handlers/start_handler.py
import logging
from telegram import Update, InputFile
from telegram.ext import ContextTypes, ConversationHandler, CommandHandler, CallbackQueryHandler, MessageHandler, filters
from keyboards.main_menu import role_selection_kb
from config import settings
from database import db
import os

logger = logging.getLogger(__name__)

CHOOSING_ROLE, ASK_PASSWORD, ASK_CLASS, ASK_FULLNAME = range(4)

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # greet and ask role
    await update.message.reply_text(
        "Assalomu alaykum! SmartSchool Bot ga xush kelibsiz.\nIltimos, rolingizni tanlang:",
        reply_markup=role_selection_kb()
    )
    return CHOOSING_ROLE

async def role_selected(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data  # e.g. "role:student"
    if not data or not data.startswith("role:"):
        await query.edit_message_text("Noma'lum tanlov.")
        return ConversationHandler.END
    role = data.split(":",1)[1]
    context.user_data["role_candidate"] = role
    await query.edit_message_text(f"Siz `{role}` rollini tanladingiz. Iltimos parolni yuboring.", parse_mode="Markdown")
    return ASK_PASSWORD

async def password_received(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (update.message.text or "").strip()
    role = context.user_data.get("role_candidate")
    ok = False
    if role == "student" and text == settings.STUDENT_PASSWORD:
        ok = True
    if role == "teacher" and text == settings.TEACHER_PASSWORD:
        ok = True
    if role == "parent" and text == settings.PARENT_PASSWORD:
        ok = True
    if role == "admin" and text == settings.ADMIN_PASSWORD:
        ok = True

    if not ok:
        await update.message.reply_text("Parol noto'g'ri. /start bilan qayta urinib ko'ring yoki parolni to'g'rilang.")
        return ASK_PASSWORD

    # save or update user with role
    tg = update.effective_user
    await db.create_or_update_user(tg.id, role, getattr(tg, "username", None))

    # send intro video if exists
    video_path = settings.INTRO_VIDEOS.get(role)
    if video_path and os.path.exists(video_path):
        try:
            await update.message.reply_video(video=InputFile(video_path), caption="Bot qanday ishlashini qisqacha video.")
        except Exception as e:
            logger.warning("Video yuborishda xatolik: %s", e)
            await update.message.reply_text("Intro video yuborilmadi — ammo davom etamiz.")
    else:
        await update.message.reply_text("Intro video topilmadi yoki yo'q — davom etamiz.")

    if role == "student":
        # ask class
        classes = await db.get_classes()
        if classes:
            cls_list = ", ".join(classes)
            await update.message.reply_text(f"Iltimos sinf nomini yozing. Mavjud sinflar: {cls_list}\n(Example: 11-A) ")
        else:
            await update.message.reply_text("Sinf ro'yxati bo'sh. Iltimos sinf nomini to'g'ri kiriting (masalan: 11-A).")
        return ASK_CLASS

    # for non-students: finish
    await update.message.reply_text("Siz muvaffaqiyatli ro‘yxatdan o‘tdingiz. /menu tugmasini bosing.")
    return ConversationHandler.END

async def student_class_received(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (update.message.text or "").strip()
    tg = update.effective_user
    # ensure class exists and set; ask fullname next
    await db.add_class(text)
    # temporarily store chosen class in user_data then ask fullname
    context.user_data["chosen_class"] = text
    await update.message.reply_text("Endi to‘liq ism-familyangizni yozing (masalan: Jamshid Qodirov):")
    return ASK_FULLNAME

async def student_fullname_received(update: Update, context: ContextTypes.DEFAULT_TYPE):
    fullname = (update.message.text or "").strip()
    tg = update.effective_user
    class_name = context.user_data.get("chosen_class")
    if not class_name:
        await update.message.reply_text("Sinf ma'lum emas — /start bilan qayta boshlang.")
        return ConversationHandler.END
    # set DB
    await db.set_user_class_fullname(tg.id, class_name, fullname)
    # fetch students in class and show
    students = await db.get_students_in_class(class_name)
    lines = []
    for s in students:
        name = s.get("fullname") or s.get("telegram_username") or "NoName"
        lines.append(f"- {name}")
    msg = f"Siz muvaffaqiyatli saqlandingiz.\nSinf: {class_name}\nSinf a'zolari:\n" + "\n".join(lines)
    await update.message.reply_text(msg + "\n/ menu uchun /menu ni bosing.")
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # /cancel handler
    await update.message.reply_text("Ro'yxatdan o'tish bekor qilindi. /start bilan qayta boshlang.")
    return ConversationHandler.END

def get_handler():
    conv = ConversationHandler(
        entry_points=[CommandHandler("start", start_command)],
        states={
            CHOOSING_ROLE: [CallbackQueryHandler(role_selected, pattern=r"^role:")],
            ASK_PASSWORD: [MessageHandler(filters.TEXT & ~filters.COMMAND, password_received)],
            ASK_CLASS: [MessageHandler(filters.TEXT & ~filters.COMMAND, student_class_received)],
            ASK_FULLNAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, student_fullname_received)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
        allow_reentry=True
    )
    return conv
