import requests
from bs4 import BeautifulSoup
from loader import db



class AdidasParser:
    def __init__(self, category):
        self.host = 'https://7saber.uz/uz'
        self.category = category


    def get_data(self):
        html = requests.get(self.host + self.category).text
        soup = BeautifulSoup(html, 'html.parser')
        box = soup.find('div', class_= 'col-12 col-sm category__page-content-right')
        products = box.find_all('div', class_='col-12 col-sm-6 col-lg-4')
        data = []
        category_name = ''
        if self.category == '/category/93':
            category_name = 'Shoes'
        elif self.category == '/category/47':
            category_name = 'Clothing'
        elif self.category == '/category/96':
            category_name = 'Accessories'

        category_id = db.get_category_id(category_name)


        for product in products:
            product_name = product.find('h4').get_text(strip=True)
            link = product.find('a').get('href')
            image = product.find('img').get('src')
            price = (product.find('p').get_text(strip=True)).replace(',5', '').replace('$', ' ')
            # str_value = price
            #
            # cleaned_string = ''.join(char for char in str_value if char.isnumeric())
            #
            # try:
            #     result_str = str(float(cleaned_string) * 12000)
            #
            # except ValueError:
            #     print(f" '{str_value}' ni floatga ozgartirib bolmaydi.")
            #     return result_str

            data.append({
                'product_name': product_name,
                'link': link,
                'image': image,
                'price': price,
                'category_id': category_id

            })

        return data
















