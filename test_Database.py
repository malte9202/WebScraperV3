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

'''
    def test_get_url(self):
        self.fail()

    def test_get_product_ids(self):
        self.fail()
    
    def test_execute_query(self):
        self.fail()

    def test_delete_product(self):
        self.fail()
    
    def test_delete_price(self):
        self.fail()
'''