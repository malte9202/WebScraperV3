from flask import Flask
from flask_restful import reqparse, Api, Resource
from Database import Database

db_connection = Database()  # init db connection
app = Flask(__name__)  # create flask app
api = Api(app)  # create api for app
parser = reqparse.RequestParser()  # init request parser

# arguments to parse for POST product
parser.add_argument('name', type=str, help='product name')
parser.add_argument('price_threshold', type=float, help='price threshold for notification')
parser.add_argument('url', type=str, help='geizhals product url')


class Products(Resource):  # products endpoint
    def get(self):  # returns product list
        raw_result = db_connection.execute_query('SELECT name, price_threshold, url FROM products;')
        result_list = []
        for product in raw_result:
            product_dict = {
                'name': product[0],
                'price_threshold': product[1],
                'url': product[2]
            }
            result_list.append(product_dict)
        result = {'products': result_list}
        return result

    def post(self):  # creates new product in db with params name, price_threshold and url
        arguments = parser.parse_args()  # parse arguments
        # get single arguments out of dict
        name = arguments['name']
        price_threshold = arguments['price_threshold']
        url = arguments['url']
        Database.insert_product(db_connection, name, price_threshold, url)
        return f'Inserted {name}, {price_threshold}, {url} into products'

    def delete(self, product_id):  # delete product from database
        Database.delete_product(db_connection, product_id)
        return f'Product with id {product_id} deleted'


class Prices(Resource):  # prices endpoint to return all prices
    def get(self):
        raw_result = db_connection.execute_query('SELECT product_id, price FROM prices;')
        result = {'prices': raw_result}
        return result


class PriceProductId(Resource):  # returns price to a product id
    def get(self, product_id):
        raw_result = db_connection.execute_query(f'SELECT price FROM prices WHERE product_id = {product_id}')
        result = {'data': raw_result}
        return result


api.add_resource(Products, '/products')  # add products endpoint
api.add_resource(Prices, '/prices')  # add prices ep
api.add_resource(PriceProductId, '/prices/<product_id>')  # add price per product_id

if __name__ == '__main__':
    app.run()

