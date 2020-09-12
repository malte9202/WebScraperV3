from Database import Database
from Scraper import Scraper
from migrations import migrate

migrate()  # runs all migrations, only new migrations are executed

database = Database()  # create db connection

product_ids = Database.get_product_ids(database)  # get product_ids from database

for product_id in product_ids:  # for each product
    url = Database.get_url(database, product_id)  # get url from database
    price = Scraper.get_price(url)  # scrape current price from web
    Database.insert_price(database, product_id, price)  # insert price in db
