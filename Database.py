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
        self.db_cursor = self.db_connection.cursor(buffered=True)

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

    def insert_product(self, name: str, url: str):
        insert_statement = 'INSERT INTO products (name, url) VALUES (%s, %s);'
        self.db_cursor.execute(insert_statement, (name, url))
        self.db_connection.commit()

    def insert_price(self, product_id: int, price: float):
        insert_statement = 'INSERT INTO prices (product_id, price) VALUES (%s, %s);'
        self.db_cursor.execute(insert_statement, (product_id, price))
        self.db_connection.commit()

    def get_url(self, product_id: int) -> str:
        query = 'SELECT url FROM products WHERE id = %s;'
        self.db_cursor.execute(query, (product_id,))
        url = self.db_cursor.fetchone()[0]
        return url

    def get_product_ids(self):
        query = 'SELECT id FROM products;'
        self.db_cursor.execute(query)
        product_ids = []
        for element in self.db_cursor.fetchall():
            product_ids.append(element[0])
        return product_ids

    def execute_query(self, query: str):
        self.db_cursor.execute(query)
        result = self.db_cursor.fetchall()
        return result

    def delete_product(self, product_id: int):
        delete_statement = 'DELETE FROM products WHERE id = %s;'
        self.db_cursor.execute(delete_statement, (product_id,))
        self.db_connection.commit()

    def delete_price(self, product_id: int):
        delete_statement = 'DELETE FROM prices WHERE product_id = %s;'
        self.db_cursor.execute(delete_statement, (product_id,))
        self.db_connection.commit()

    def __del__(self):
        self.db_connection.close()
