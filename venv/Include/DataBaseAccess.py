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


if __name__ == '__main__':
    sql = "INSERT INTO Users (ID,Name) VALUES (%s,%s)"
    val = (1, "Bot")
    # user_cursor.execute(sql, val)
    # user_database.commit()
    # print(user_cursor.lastrowid)
