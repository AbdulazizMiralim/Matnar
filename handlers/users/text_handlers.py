from telebot.types import Message, ReplyKeyboardRemove

from loader import bot, db
from keyboards.default import *
from keyboards.inlines import *
from states import RegisterState


@bot.message_handler(commands=['start', 'help'])
def reaction_start(message: Message):
    chat_id = message.chat.id
    if message.text == '/start':
        db.insert_telegram_id(chat_id)
        bot.send_message(chat_id, "Salom,Xizmatlarni tanlang", reply_markup=main_menu_btn())


# @bot.message_handler(commands=['start', 'help'])
# def reaction_start(message: Message):
#     chat_id = message.chat.id
#     if message.text == '/help':
#         db.insert_telegram_id(chat_id)
#         bot.send_message(chat_id, "🚨Tezda bog'lanish", reply_markup=main_menu_btn())
#
#
# @bot.message_handler(func=lambda message: message.text == '/help')
# def reaction_emergency(message: Message):
#     chat_id = message.chat.id
#     if db.check_user_id(chat_id):
#         text = 'Tezda aloqa uchun nomer!'
#         bot.send_message(chat_id, text)



@bot.message_handler(func=lambda message: message.text == '🛍Menu')
def reaction_manu(message: Message):
    chat_id = message.chat.id
    if db.check_user_id(chat_id):
        text = 'Menu'
        markup = categories_btn()

    else:
        text = "Uzur sir ro'yxatdan o'tmagansiz"
        markup = register_btn()
    bot.send_message(chat_id, text, reply_markup=markup)


@bot.message_handler(func=lambda message: message.text == '✍️Registration')
def reaction_register(message: Message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    bot.set_state(user_id, RegisterState.name, chat_id)
    bot.send_message(chat_id, 'Ismingizni kiriting: ', reply_markup=ReplyKeyboardRemove())

@bot.message_handler(content_types=['text'], state=RegisterState.name)
def reaction_name(message: Message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    with bot.retrieve_data(user_id, chat_id) as data:
        data['name'] = message.text.capitalize()
    bot.set_state(user_id, RegisterState.lastname, chat_id)
    bot.send_message(chat_id, 'Familiyangizni kiriting: ', reply_markup=ReplyKeyboardRemove())

@bot.message_handler(content_types=['text'], state=RegisterState.lastname)
def reaction_lastname(message: Message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    with bot.retrieve_data(user_id, chat_id) as data:
        data['lastname'] = message.text.capitalize()
    bot.set_state(user_id, RegisterState.contact, chat_id)
    bot.send_message(chat_id, 'Telefon raqamingizni kiriting <b>+998XXXXXXXXX</b> ',
                     reply_markup=send_contact_btn(), parse_mode='html')

@bot.message_handler(content_types=['contact', 'text'], state=RegisterState.contact)
def reaction_contact(message: Message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    with bot.retrieve_data(user_id, chat_id) as data:

        if message.content_type == 'contact':
            data['contact'] = message.contact.phone_number
            bot.set_state(user_id, RegisterState.birthdate, chat_id)
            bot.send_message(chat_id, 'Tugilgan kuningizni kiriting: dd.mm.yyyy ',
                             reply_markup=ReplyKeyboardRemove())
        else:
            import re
            if re.match(r'\+998(9(0|1|3|4|5|7|8|9)|33|20|77|88|55)\d{7}$', message.text):
                data['contact'] = message.text
                bot.set_state(user_id, RegisterState.birthdate, chat_id)
                bot.send_message(chat_id, 'Tugilgan kuningizni kiriting: dd.mm.yyyy ',
                                 reply_markup=ReplyKeyboardRemove())
            else:
                bot.set_state(user_id, RegisterState.contact, chat_id)
                bot.send_message(chat_id, 'Telefon raqam notogri kiritildi qaytadan kiriting!',
                                 reply_markup=send_contact_btn())

@bot.message_handler(content_types=['text'], state=RegisterState.birthdate)
def reaction_birthdate(message: Message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    import re
    if re.match(r"^(?:0[1-9]|[12]\d|3[01])([\/.-])(?:0[1-9]|1[012])\1(?:19|20)\d\d$", message.text):
        with bot.retrieve_data(user_id, chat_id) as data:
            data['birthdate']= message.text
            name = data['name']
            lastname = data['lastname']
            contact = data  ['contact']
            bot.set_state(user_id, RegisterState.submit, chat_id)
            bot.send_message(chat_id, f"""Ma'lumotni tekshiring:
Ism: {name}
Familiya: {lastname}
Telefon: {contact}
Tugilgan kun: {message.text}""", reply_markup=submit_btn())
    else:
        bot.set_state(user_id, RegisterState.birthdate, chat_id)
        bot.send_message(chat_id, ' Tugilgan kun xato. Boshidan kiriting: dd.mm.yyyy',
                         reply_markup=ReplyKeyboardRemove())


@bot.message_handler(content_types=['text'], state=RegisterState.submit)
def reaction_submit(message: Message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    if message.text == "To'gri✅":
      with bot.retrieve_data(user_id, chat_id) as data:
            name, lastname, contact, birthdate = data.values()
            db.update_user_info(name, lastname, contact, birthdate, chat_id)
      bot.send_message(chat_id, "Ma'lumotlar saqlandi!", reply_markup=main_menu_btn())
      bot.delete_state(user_id, chat_id)
    else:
        bot.delete_state(user_id, chat_id)
        bot.set_state(user_id, RegisterState.name, chat_id)
        bot.send_message(chat_id, "Ismingizni qaytadan kiriting", reply_markup=ReplyKeyboardRemove)


@bot.message_handler(func=lambda message: message.text == 'Asosiy Menu')
def reaction_main_menu(message: Message):
    chat_id = message.chat.id
    bot.send_message(chat_id, message.text, reply_markup=main_menu_btn())


@bot.message_handler(func=lambda message: message.text in db.get_all_categories())
def reaction_category(message: Message):
    chat_id = message.chat.id
    bot.send_message(chat_id, message.text, reply_markup=ReplyKeyboardRemove())
    bot.send_message(chat_id, message.text, reply_markup=products_pagination_btns(message.text))





































