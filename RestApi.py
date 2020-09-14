# import required flask extensions
from flask import Flask
from flask_restful import reqparse, Api, Resource
# import Database class
from Database import Database

db_connection = Database()  # init db connection
app = Flask(__name__)  # create flask app
api = Api(app)  # create api for flask app

parser = reqparse.RequestParser()  # init request parser
# arguments to parse for POST product
parser.add_argument('name', type=str, help='product name')
parser.add_argument('price_threshold', type=float, help='price threshold for notification')
parser.add_argument('url', type=str, help='geizhals product url')


class ProductList(Resource):  # class for list of products
    def get(self):
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


class CreateProduct(Resource):  # class to add a product
    def post(self):
        arguments = parser.parse_args()  # parse arguments
        # get single arguments out of dict
        name = arguments['name']
        price_threshold = arguments['price_threshold']
        url = arguments['url']
        Database.insert_product(db_connection, name, price_threshold, url)
        return f'Inserted: name: {name} |price_threshold: {price_threshold} |url: {url}'


class Product(Resource):  # class to delete (and edit product)
    def get(self, product_id):
        result = db_connection.execute_query(f'SELECT id, name, price_threshold, url FROM products WHERE id = {product_id}')
        return result

    def delete(self, product_id):  # delete product
        Database.delete_product(db_connection, product_id)
        return f'Product with id {product_id} deleted'


class PriceList(Resource):  # class for price list
    def get(self):
        raw_result = db_connection.execute_query('SELECT product_id, price FROM prices;')
        result = {'prices': raw_result}
        return result


class Price(Resource):  # class for single price
    def get(self, product_id):
        raw_result = db_connection.execute_query(f'SELECT product_id, price FROM prices WHERE product_id = {product_id}')
        result = {'price': raw_result}
        return result


api.add_resource(ProductList, '/productlist')  # add productlist endpoint
api.add_resource(CreateProduct, '/product/create')  # add create endpoint
api.add_resource(Product, '/product/<product_id>')  # add product endpoint
api.add_resource(PriceList, '/prices')  # add pricelist endpoint
api.add_resource(Price, '/price/<product_id>')  # add price endpoint

if __name__ == '__main__':
    app.run()
