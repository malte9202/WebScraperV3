from Database import Database
from Scraper import Scraper

database = Database()

Database.create_products_table(database)

Database.create_prices_table(database)

Database.insert_product(database, 'Apple iPad 2019 128GB',
                        'https://geizhals.de/apple-ipad-10-2-128gb-mw772fd-a-mw772ll-a-a2132800.html')


product_ids = Database.get_product_ids(database)

for product_id in product_ids:
    url = Database.get_url(database, product_id)
    price = Scraper.get_price(url)
    Database.insert_price(database, product_id, price)
