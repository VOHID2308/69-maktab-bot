from telegram import ReplyKeyboardMarkup, KeyboardButton

def admin_main_menu():
    buttons = [
        [KeyboardButton("📋 Foydalanuvchilar ro‘yxati")],
        [KeyboardButton("➕ Yangi sinf qo‘shish")],
        [KeyboardButton("📊 Hisobotlar")],
        [KeyboardButton("🔙 Chiqish")],
    ]
    return ReplyKeyboardMarkup(buttons, resize_keyboard=True)
