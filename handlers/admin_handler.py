from telegram import Update
from telegram.ext import ContextTypes, CommandHandler
from keyboards.admin_keyboards import admin_main_menu
from config import settings

async def admin_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    tg = update.effective_user

    # faqat admin uchun ruxsat
    if str(tg.id) != str(settings.ADMIN_ID):
        await update.message.reply_text("🚫 Siz admin emassiz.")
        return

    await update.message.reply_text(
        "👨‍💼 Admin paneliga xush kelibsiz!",
        reply_markup=admin_main_menu()
    )

def get_handlers():
    return [CommandHandler("menu", admin_menu)]
