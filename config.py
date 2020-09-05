import os  # import operating system functions
from dotenv import load_dotenv, find_dotenv  # import dotenv module to use .env file for credentials

load_dotenv(find_dotenv())  # find .env file

user = os.environ.get('USERNAME')
password = os.environ.get('PASSWORD')
host = os.environ.get('HOST')
database = os.environ.get('DATABASE')
