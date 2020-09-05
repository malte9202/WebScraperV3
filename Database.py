import mysql.connector as mysql
from config import host, user, password, database


class Database(object):
    def __init__(self):
        self.db_connection = mysql.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        self.db_cursor = self.db_connection.cursor()

    def create_products_table(self):
        create_statement = 'CREATE TABLE IF NOT EXISTS products (id INT AUTO_INCREMENT PRIMARY KEY,' \
                           'name VARCHAR(255),' \
                           'url VARCHAR(255));'
        self.db_cursor.execute(create_statement)
        self.db_connection.commit()

    def create_prices_table(self):
        create_statement = 'CREATE TABLE IF NOT EXISTS prices (product_id INT NOT NULL,' \
                           'price FLOAT NOT NULL,' \
                           'scraped_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP);'
        self.db_cursor.execute(create_statement)
        self.db_connection.commit()

    def insert_product(self, name, url):
        insert_statement = 'INSERT INTO products (name, url) VALUES (%s, %s);'
        self.db_cursor.execute(insert_statement, (name, url))
        self.db_connection.commit()

    def insert_price(self, product_id, price):
        insert_statement = 'INSERT INTO prices (product_id, price) VALUES (%s, %s);'
        self.db_cursor.execute(insert_statement, (product_id, price))
        self.db_connection.commit()

    def __del__(self):
        self.db_connection.close()
