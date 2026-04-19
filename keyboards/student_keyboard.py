# keyboards/student_keyboard.py
from telegram import ReplyKeyboardMarkup

def student_menu_kb():
    kb = [
        ["Bugungi darslar", "Uy vazifalar"],
        ["Baholarim", "Davomat"],
        ["/sinf", "/menu"]
    ]
    return ReplyKeyboardMarkup(kb, resize_keyboard=True)
