from loader import bot, db

from parsing_codes import AdidasParser


db.create_users_table()
db.create_categories()
db.create_products()
db.create_gender()


# categories = ['Shoes', 'Clothing', 'Accessories']
# for category in categories:
#     db.insert_categories(category)
#
#
# categories_links = ['/category/93','/category/47', '/category/96']
# categories_data =[AdidasParser(i).get_data() for i in categories_links]
#
# for items in categories_data:
#     for product in items:
#         db.insert_products(**product)


import handlers




if __name__ == '__main__':
    print('Bot ishga tushdi...')
    print('https://t.me/matnarbot')
    bot.infinity_polling()