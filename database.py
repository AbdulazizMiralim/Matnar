import psycopg2

class DataBase:
    def __init__(self, dbname, user, host, password):
        self.database=psycopg2.connect(
            database=dbname,
            user=user,
            host=host,
            password=password
        )

    def manage(self, sql, *args, commit:bool=False, fetchone:bool=False, fetchall:bool=False):
        with self.database as db:
            cursor = db.cursor()
            cursor.execute(sql, args)
            if commit:
                return db.commit()
            elif fetchone:
                return cursor.fetchone()
            elif fetchall:
                return cursor.fetchall()


    def create_users_table(self):
        sql = '''CREATE TABLE IF NOT EXISTS users(
        telegram_id BIGINT PRIMARY KEY,
        name VARCHAR (30),
        lastname VARCHAR(30),
        contact VARCHAR(30) UNIQUE,
        birthdate DATE
        )'''

        self.manage(sql, commit=True)

    def check_user_id(self, telegram_id):
        sql = '''SELECT * FROM users WHERE telegram_id = %s'''
        return None not in self.manage(sql, telegram_id, fetchone=True)

    def insert_telegram_id(self,telegram_id):
        sql = '''INSERT INTO users(telegram_id) VALUES(%s) ON CONFLICT DO NOTHING '''
        self.manage(sql, (telegram_id,), commit=True)



    def update_user_info(self, name, lastname, contact, birthdate, telegram_id):
        sql = '''UPDATE users SET name=%s, lastname=%s, contact=%s, birthdate=%s WHERE telegram_id=%s'''
        self.manage(sql, name, lastname, contact, birthdate, telegram_id, commit=True)


    def create_categories(self):
        sql = '''CREATE TABLE IF NOT EXISTS categories(
        category_id SERIAL PRIMARY KEY,
        category VARCHAR(50) UNIQUE
        )'''
        self.manage(sql, commit=True)


    def create_products(self):
        sql = '''CREATE TABLE IF NOT EXISTS products(
        product_id SERIAL PRIMARY KEY,
        product_name TEXT UNIQUE,
        price INTEGER,
        image TEXT,
        link TEXT,
        category_id INTEGER REFERENCES categories(category_id) 
        )'''
        self.manage(sql, commit=True)

    def create_gender(self ):
        sql = '''CREATE TABLE IF NOT EXISTS gender(
        male TEXT,
        female TEXT
        )'''
        self.manage(sql, commit=True)



    def insert_categories(self, category):
        sql = '''INSERT INTO categories(category) VALUES (%s) ON CONFLICT DO NOTHING'''
        self.manage(sql, (category), commit=True)


    def get_category_id(self, category):
        sql = '''SELECT category_id FROM categories WHERE category=%s'''
        return self.manage(sql, category, fetchone=True)


    def insert_products(self, product_name, price, image, link, category_id):
        sql = '''INSERT INTO products(product_name, price, image, link, category_id) 
        VALUES (%s, %s, %s, %s, %s) ON CONFLICT DO NOTHING'''
        self.manage(sql, product_name, price, image, link, category_id, commit=True)


    def get_all_categories(self):
        sql = '''SELECT category FROM categories'''
        return [item[0] for item in self.manage(sql, fetchall=True)]

    # def get_products_by_category(self, category):
    #     sql = '''   SELECT * FROM products WHERE category_id = (SELECT category_id FROM categories WHERE category = %s) '''
    #     return self.manage(sql, category, fetchall=True)

    def get_products_by_category_pagination(self, category, offset, limit):
        sql = '''SELECT * FROM products WHERE category_id = (SELECT category_id FROM categories WHERE category = %s)
        OFFSET %s
        LIMIT %s'''
        return self.manage(sql, category, offset, limit, fetchall=True)

    def get_count_products(self, category):
        sql = '''SELECT count(product_id) FROM products 
        WHERE category_id = (SELECT category_id FROM categories WHERE category = %s)'''
        return self.manage(sql, category, fetchone=True)[0]

    def get_product_info(self, product_id):
        sql = '''SELECT * FROM products WHERE product_id = %s'''
        return self.manage(sql, product_id, fetchone=True)

    def get_category_by_id(self, category_id):
        sql = '''SELECT category FROM categories WHERE category_id = %s'''
        return self.manage(sql, category_id, fetchone=True)[0]











