# keyboards/main_menu.py
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

def role_selection_kb():
    keyboard = [
        [InlineKeyboardButton("O'quvchi 👩‍🎓", callback_data="role:student"),
         InlineKeyboardButton("O'qituvchi 👨‍🏫", callback_data="role:teacher")],
        [InlineKeyboardButton("Ota-ona 👪", callback_data="role:parent"),
         InlineKeyboardButton("Admin ⚙️", callback_data="role:admin")]
    ]
    return InlineKeyboardMarkup(keyboard)
