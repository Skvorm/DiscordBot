import os

import mysql.connector
from dotenv import load_dotenv


class DataBaseAccess:
    load_dotenv()
    host = os.getenv('DB_HOST')
    user = os.getenv('DB_USER')
    password = os.getenv('DB_PASS')
    database = os.getenv('DB_NAME')
    user_database = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=database
    )
    user_cursor = user_database.cursor()

