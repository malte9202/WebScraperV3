from unittest import TestCase
from Database import Database


class TestDatabase(TestCase):
    def test_create_products_table(self):
        test_database = Database()
        Database.create_products_table(test_database)
        test_query = 'SHOW TABLES;'
        self.assertIn(('products',), Database.execute_query(test_database, test_query))

    def test_create_prices_table(self):
        test_database = Database()
        Database.create_prices_table(test_database)
        test_query = 'SHOW TABLES;'
        self.assertIn(('prices',), Database.execute_query(test_database, test_query))

    def test_insert_product(self):
        test_database = Database()
        Database.insert_product(test_database, 'test product', 'https://testproducturl.com')
        test_query = 'SELECT url FROM products WHERE name = \'test product\';'
        self.assertEqual([('https://testproducturl.com',)], Database.execute_query(test_database, test_query))
        test_id = Database.execute_query(test_database, 'SELECT id FROM products WHERE name = \'test product\';')[0][0]
        Database.delete_product(test_database, test_id)

    def test_insert_price(self):
        test_database = Database()
        Database.insert_product(test_database, 'test price product', 'https://testpriceurl.com')
        test_id = Database.execute_query(test_database,
                                         'SELECT id FROM products WHERE name = \'test price product\';')[0][0]
        Database.insert_price(test_database, test_id, 9999.99)
        test_query = f'SELECT price FROM prices WHERE product_id = {test_id};'
        self.assertEqual([(9999.99,)], Database.execute_query(test_database, test_query))
        Database.delete_price(test_database, test_id)
        Database.delete_product(test_database, test_id)

    def test_get_url(self):
        test_database = Database()
        Database.insert_product(test_database, 'test get url', 'https://testgeturl.com')
        test_id = Database.execute_query(test_database,
                                         'SELECT id FROM products WHERE name = \'test get url\';')[0][0]
        test_query = f'SELECT url FROM products WHERE id = {test_id};'
        self.assertEqual([('https://testgeturl.com',)], Database.execute_query(test_database, test_query))
        Database.delete_product(test_database, test_id)

    def test_get_product_ids(self):
        test_database = Database()
        product_ids = Database.get_product_ids(test_database)
        for product_id in product_ids:
            self.assertEqual(type(product_id), int)

    def test_execute_query(self):
        test_database = Database()
        count_result = Database.execute_query(test_database, 'SELECT COUNT(id) FROM products;')[0][0]
        self.assertEqual(type(count_result), int)
        list_result = Database.execute_query(test_database, 'SELECT * FROM prices;')
        self.assertEqual(type(list_result), list)

    def test_delete_product(self):
        test_database = Database()
        Database.insert_product(test_database, 'test delete', 'https://testdelete.com')
        test_id = Database.execute_query(test_database, 'SELECT id FROM products WHERE name = \'test delete\';')[0][0]
        Database.delete_product(test_database, test_id)
        test_result = Database.execute_query(test_database,
                                             'SELECT COUNT(1) FROM products where name = \'test delete\';')[0][0]
        self.assertEqual(test_result, 0)

    def test_delete_price(self):
        test_database = Database()
        Database.insert_product(test_database, 'test delete', 'https://testdelete.com')
        test_id = Database.execute_query(test_database, 'SELECT id FROM products WHERE name = \'test delete\';')[0][0]
        Database.insert_price(test_database, test_id, 777.77)
        Database.delete_price(test_database, test_id)
        test_result = Database.execute_query(test_database,
                                             f'SELECT COUNT(1) FROM prices WHERE product_id = {test_id};')[0][0]
        self.assertEqual(test_result, 0)
        Database.delete_product(test_database, test_id)



