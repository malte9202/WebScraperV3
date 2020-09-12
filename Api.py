from flask import Flask, request
from flask_restful import Resource, Api
import mysql
import json
from flask import jsonify
from Database import Database

db_connection = Database()
app = Flask(__name__)
api = Api(app)


class Products(Resource):
    @staticmethod
    def get():
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

    @staticmethod
    def post(name, price_threshold, url):
        db_connection.insert_product(name, price_threshold, url)
        return 'sucess'


class Prices(Resource):
    @staticmethod
    def get():
        raw_result = db_connection.execute_query('SELECT product_id, price FROM prices;')
        result = {'prices': raw_result}
        return result


class PriceProductId(Resource):
    @staticmethod
    def get(product_id):
        raw_result = db_connection.execute_query(f'SELECT price FROM prices WHERE product_id = {product_id}')
        result = {'data': raw_result}
        return result


api.add_resource(Products, '/products')  # Route_1
api.add_resource(Prices, '/prices')  # Route_2
api.add_resource(PriceProductId, '/prices/<product_id>')  # Route_3

if __name__ == '__main__':
    app.run()

