from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup

from loader import db

# def get_products_btn(category):
#     products = db.get_products_by_category(category)
#     markup = InlineKeyboardMarkup(row_width=1)
#     for item in products:
#         markup.add(InlineKeyboardButton(item[1], callback_data=f"product| {item[0]}"))
#     return markup


def products_pagination_btns(category, page=1):
    markup = InlineKeyboardMarkup(row_width=1)
    limit = 5
    count_products = db.get_count_products(category)
    # count_products =  count_products[0] if isinstance(count_products, tuple) else count_products
    # max_page = count_products // limit if count_products % limit == 0 else count_products // limit + 1
    max_page = count_products // limit if count_products % limit == 0 else count_products // limit + 1
    offset = (page - 1) * limit

    produsts = db.get_products_by_category_pagination(category, offset, limit)

    for item in produsts:
        markup.add(InlineKeyboardButton(item[1], callback_data=f"product|{item[0]}"))


    preview_btn = InlineKeyboardButton("⏮", callback_data='preview')
    page_btn = InlineKeyboardButton(page, callback_data=f"page|{category}")
    next_btn = InlineKeyboardButton("⏭", callback_data='next')
    if page == 1:
        markup.row(page_btn, next_btn)
    elif 1 < page < max_page:
        markup.row(preview_btn, page_btn, next_btn)
    elif page == max_page:
        markup.row(preview_btn, page_btn)

    markup.row(InlineKeyboardButton("🔙 Back", callback_data='back_categories'),
               InlineKeyboardButton("Asosiy Menu", callback_data='main_menu'))
    return markup

def product_btn(category_id, product_id, page, quantity=1):
    items = [
        InlineKeyboardButton("➖", callback_data='minus'),
        InlineKeyboardButton(quantity, callback_data=f'quantity|{page}'),
        InlineKeyboardButton("➕", callback_data='plus')
    ]
    card_items = [
        InlineKeyboardButton("Savatga qo'shish", callback_data=f'add_cart|{product_id}'),
        InlineKeyboardButton("Savat🛒", callback_data="show_cart")
    ]
    return InlineKeyboardMarkup(keyboard=[
        items,
        card_items,
        [InlineKeyboardButton('🔙 Back', callback_data=f"back_cat_id|{category_id}"),
         InlineKeyboardButton("Asosiy Menu", callback_data='main_menu')]
    ])



def cart_btn(data: dict):
    markup = InlineKeyboardMarkup(row_width=1)
    for product_name, items in data.items():
        product_id = items['product_id']
        markup.add(InlineKeyboardButton(f"❌ {product_name}", callback_data=f"remove|{product_id}"))

    markup.row(InlineKeyboardButton('Tozalash 🔁', callback_data='clear_cart'),
               InlineKeyboardButton('Tasdiqlash ✅', callback_data='submit'))
    markup.row(InlineKeyboardButton('Kategoriyalar', callback_data='back_categories'))
    return markup















