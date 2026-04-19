# keyboards/shared_kb.py
from telegram import ReplyKeyboardMarkup

def back_menu_kb():
    return ReplyKeyboardMarkup([["/menu", "/start"]], resize_keyboard=True)
