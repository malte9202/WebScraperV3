from Database import Database
from Scraper import Scraper

database = Database()

Database.create_products_table(database)

Database.create_prices_table(database)

'''
Database.insert_product(database, 'MacBook Air 13 2020',
                        'https://geizhals.de/apple-macbook-air-space-gray-mwtj2d-a-a2255044.html')
'''

product_ids = Database.get_product_ids(database)

for product_id in product_ids:
    url = Database.get_url(database, product_id)
    price = Scraper.get_price(url)
    Database.insert_price(database, product_id, price)
