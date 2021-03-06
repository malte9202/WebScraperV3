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

    def execute_migration(self, migrations):
        self.db_cursor.execute('CREATE TABLE IF NOT EXISTS migrations '
                               '(id INT AUTO_INCREMENT PRIMARY KEY, '
                               'name VARCHAR(255), '
                               'executed BOOLEAN DEFAULT FALSE);')
        for migration in migrations:
            executed_migrations_raw = self.execute_query('SELECT name FROM migrations WHERE executed = 1;')
            executed_migrations = []
            for executed_migration in executed_migrations_raw:
                executed_migrations.append(executed_migration[0])
            if migration not in executed_migrations:
                self.db_cursor.execute('INSERT INTO migrations (name) VALUES (%s);', (migration,))
                self.db_cursor.execute(migrations[migration])
                self.db_connection.commit()
                self.db_cursor.execute('UPDATE migrations '
                                       'SET executed = 1 '
                                       'WHERE name = (%s);', (migration,))
                self.db_connection.commit()
            else:
                pass

    def insert_product(self, name: str, price_threshold: float, url: str):
        insert_statement = 'INSERT INTO products (name, price_threshold, url) VALUES (%s, %s, %s);'
        self.db_cursor.execute(insert_statement, (name, price_threshold, url))
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
