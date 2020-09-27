import os  # import operating system functions
from dotenv import load_dotenv, find_dotenv  # import dotenv module to use.env file for credentials

load_dotenv(find_dotenv())  # find .env file and load it

user = os.environ.get('USERNAME')  # get username from .env
password = os.environ.get('PASSWORD')  # get password from .env file
host = os.environ.get('HOST')  # get host from .env file
database = os.environ.get('DATABASE')  # get database from .env file
