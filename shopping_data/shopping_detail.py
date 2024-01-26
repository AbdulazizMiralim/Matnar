from telebot.types import LabeledPrice
from .shopping_product import Product

def generate_product_invoice(product_data):
    query = Product(
        title= 'Matnar.uz',
        description = '\n'.join([title for title in product_data]),
        currency='USD',
        prices=[LabeledPrice(
            label=f"{title}",
            amount=int(product_data[title]['quantity']) * int(product_data[title]['price']))
             for title in product_data],
        start_parameter='create_invoice_products',
        need_name=True,
        need_phone_number=True,
        is_flexible=False
    )
    return query






