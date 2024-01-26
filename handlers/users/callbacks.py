from telebot.types import CallbackQuery
from keyboards.default import *
from keyboards.inlines import *

from loader import db, bot
from states import CartState
from shopping_data.shopping_detail import generate_product_invoice


@bot.callback_query_handler(func=lambda call: call.data == 'main_menu')
def reaction_main_menu(call: CallbackQuery):
    chat_id = call.message.chat.id
    bot.delete_message(chat_id, call.message.id)
    bot.send_message(chat_id, 'Asosiy Menu', reply_markup=main_menu_btn())

@bot.callback_query_handler(func=lambda call: call.data == 'next')
def reaction_next(call: CallbackQuery):
    chat_id = call.message.chat.id
    keyboard_list = call.message.reply_markup.keyboard[-2]
    for item in keyboard_list:
        if 'page' in item.callback_data:
            category = item.callback_data.split("|")[1]
            page = int(item.text)
            page += 1
            bot.edit_message_reply_markup(chat_id, call.message.id, reply_markup=products_pagination_btns(category, page))


@bot.callback_query_handler(func=lambda call: call.data == 'preview')
def reaction_preview(call: CallbackQuery):
    chat_id = call.message.chat.id
    keyboard_list = call.message.reply_markup.keyboard[-2]
    for item in keyboard_list:
        if 'page' in item.callback_data:
            category = item.callback_data.split("|")[1]
            page = int(item.text)
            page -= 1
            bot.edit_message_reply_markup(chat_id, call.message.id,
                                          reply_markup=products_pagination_btns(category, page))



@bot.callback_query_handler(func=lambda call: 'page' in call.data)
def reaction_page (call: CallbackQuery):
    keyboard_list = call.message.reply_markup.keyboard[-2]
    for item in keyboard_list:
        if 'page' in item.callback_data:
            page = int(item.text)
            bot.answer_callback_query(call.id, f"Siz {page}chi betdasiz")

@bot.callback_query_handler(func=lambda call: call.data == 'back_categories')
def reaction_back_categories(call: CallbackQuery):
    chat_id = call.message.chat.id
    bot.delete_message(chat_id, call.message.id)
    bot.send_message(chat_id, "Categories", reply_markup=categories_btn())


@bot.callback_query_handler(func=lambda call: 'product' in call.data)
def reaction_product(call: CallbackQuery):
    chat_id = call.message.chat.id
    product_id = call.data.split("|")[1]
    product = db.get_product_info(product_id)
    keyboard_list = call.message.reply_markup.keyboard[-2]
    page = 1
    for item in keyboard_list:
        if 'page' in item.callback_data:
            page = int(item.text)
    product_name, price, image, link, category_id = product[1:]
    bot.delete_message(chat_id, call.message.id)
    bot.send_photo(chat_id, image, caption=f"""{product_name}
Narxi: {price}
<a href="{link}">Ba'atfsil ma'lumot</a>""", parse_mode='html', reply_markup=product_btn(category_id, product_id, page))


@bot.callback_query_handler(func=lambda call: 'back_cat_id' in call.data)
def reaction_back_cat_id(call: CallbackQuery):
    chat_id = call.message.chat.id
    page = int(call.message.reply_markup.keyboard[0][1].callback_data.split('|')[1])
    category_id = call.data.split('|')[1]
    category = db.get_category_by_id(category_id)
    bot.delete_message(chat_id, call.message.id)
    bot.send_message(chat_id, category, reply_markup=products_pagination_btns(category, page))


@bot.callback_query_handler(func=lambda call: call.data in ['plus', 'minus'])
def reaction_plus(call: CallbackQuery):
    chat_id = call.message.chat.id
    quantity =int(call.message.reply_markup.keyboard[0][1].text)

    page = int(call.message.reply_markup.keyboard[0][1].callback_data.split('|')[1])
    category_id = int(call.message.reply_markup.keyboard[-1][0].callback_data.split('|')[1])
    product_id = int(call.message.reply_markup.keyboard[-2][0].callback_data.split('|')[1])
    if call.data == 'plus':
        quantity += 1
        bot.edit_message_reply_markup(chat_id, call.message.id,
                                      reply_markup=product_btn(category_id, product_id, page, quantity))
    else:
        if quantity > 1:
            quantity -= 1
            bot.edit_message_reply_markup(chat_id, call.message.id,
                                          reply_markup=product_btn(category_id, product_id, page, quantity))
        else:
            bot.answer_callback_query(call.id, "Siz eng kamida 1 ta mahsulot olishingiz kerak!", show_alert=True)


@bot.callback_query_handler(func=lambda call: 'quantity' in call.data)
def reaction_quantity(call: CallbackQuery):
    quantity = int(call.message.reply_markup.keyboard[0][1].text)
    bot.answer_callback_query(call.id, f"Mahsulotdan hozircha: {quantity}ta")


@bot.callback_query_handler(func=lambda call: 'add_cart' in call.data)
def reaction_add_cart(call: CallbackQuery):
    chat_id = call.message.chat.id
    user_id = call.from_user.id
    bot.set_state(user_id, CartState.cart, chat_id)
    product_id = call.data.split('|')[1]
    product = db.get_product_info(product_id)
    product_name, price = product[1], product[2]
    quantity = int(call.message.reply_markup.keyboard[0][1].text)
    with bot.retrieve_data(user_id, chat_id) as data:
        if data.get('cart'):
            data['cart'][product_name] = {
                'product_id': product_id,
                'price': price,
                'quantity': quantity
            }
            bot.answer_callback_query(call.id, "Qo'shildi!")
        else:
            data['cart'] = {
                product_name: {
                    'product_id': product_id,
                    'price': price,
                    'quantity': quantity
                }
            }
            bot.answer_callback_query(call.id, "Qo'shildi!")


@bot.callback_query_handler(func=lambda call: call.data == 'show_cart')
def reaction_show_cart(call: CallbackQuery):
    chat_id = call.message.chat.id
    user_id = call.from_user.id
    with bot.retrieve_data(user_id, chat_id) as data:
        res = get_cart_text_markup(data)
        text = res['text']
        markup = res['markup']
    bot.delete_message(chat_id, call.message.id)
    bot.send_message(chat_id, text, reply_markup=markup)


@bot.callback_query_handler(func=lambda call: 'remove' in call.data)
def reaction_remove(call: CallbackQuery):
    chat_id = call.message.chat.id
    user_id = call.from_user.id
    product_id = int(call.data.split('|')[1])
    with bot.retrieve_data(user_id, chat_id) as data:
        keys = [item for item in data['cart'].keys()]
        for product_name in keys:
            if int(data['cart'][product_name]['product_id']) == product_id:
                del data['cart'][product_name]
    res = get_cart_text_markup(data)
    text = res['text']
    markup = res['markup']
    bot.delete_message(chat_id, call.message.id)
    bot.send_message(chat_id, text, reply_markup=markup)


def get_cart_text_markup(data: dict):
    text = "Savat:\n"
    total_price = 0
    for product_name, items in data['cart'].items():
        product_price = items['price']
        quantity = items['quantity']
        price = int(product_price) * int(quantity)
        total_price += price
        text += f"""{product_name}
Narxi: {quantity} * {product_price} = {price} USD/$\n"""

        if total_price == 0:
            text = "Savatingiz bo'sh!"
            markup = main_menu_btn()
        else:
            text += f"\nUmumiy narx: {total_price} USD/$"
            markup = cart_btn(data['cart'])
        return {'markup': markup, 'text': text}


@bot.callback_query_handler(func=lambda call: call.data == 'clear_cart')
def reaction_clear_cart(call: CallbackQuery):
    chat_id = call.message.chat.id
    user_id = call.from_user
    bot.delete_state(user_id, chat_id)
    bot.delete_message(chat_id, call.message.id)
    bot.send_message(chat_id, "Savat bo'sh!", reply_markup=main_menu_btn())



@bot.callback_query_handler(func=lambda call: call.data == 'submit')
def reaction_submit(call: CallbackQuery):
    chat_id = call.message.chat.id
    user_id = call.from_user.id
    with bot.retrieve_data(user_id, chat_id) as data:
        bot.send_invoice(chat_id, **generate_product_invoice(data['cart']).generate_invoice(),
                         invoice_payload='Matnar.uz')


