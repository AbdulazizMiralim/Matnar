from telebot.types import ReplyKeyboardMarkup, KeyboardButton

from loader import db

def main_menu_btn():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(
        KeyboardButton('🛍Menu'),
        KeyboardButton('🛒Cart'),
        KeyboardButton('⚙️Settings'),
        KeyboardButton('📞Emergency call')
    )
    return markup

def register_btn():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(KeyboardButton("✍️Registration"))
    return markup

def send_contact_btn():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(KeyboardButton("📞Send contact", request_contact=True))
    return markup

def submit_btn():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(KeyboardButton("To'gri✅"), KeyboardButton('Qayta kiritish🔁'))
    return markup

def categories_btn():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    for item in db.get_all_categories():
        markup.add(KeyboardButton(item))
    markup.add(KeyboardButton("Asosiy Menu"))
    return markup













