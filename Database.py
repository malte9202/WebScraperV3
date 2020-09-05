import mysql.connector as mysql  # import mysql connector
from config import host, user, password, database  # import credentials, host and database from config file


# function to create database connection
def connect():
    try:
        db = mysql.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        return db
    except mysql.Error as err:
        print(err)


connection = connect()
cursor = connection.cursor(buffered=True)
