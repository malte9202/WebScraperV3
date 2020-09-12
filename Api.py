from flask import Flask, request
from flask_restful import Resource, Api
import mysql
from json import dumps
from flask import jsonify
from Database import Database

db_connection = Database()
app = Flask(__name__)
api = Api(app)


class Products(Resource):
    @staticmethod
    def get():
        raw_result = db_connection.execute_query('SELECT name, url FROM products;')
        result = {'products': raw_result}
        return jsonify(result)


api.add_resource(Products, '/products')  # Route_1

if __name__ == '__main__':
    app.run()

