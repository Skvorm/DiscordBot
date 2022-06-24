import os
import sqlite3


class DataBaseAccess:
    cur = ""

    count = 0

    # get user
    # put user
    # get user_score
    # put user_score (increment,set)
    def __init__(self):
        self.count = 2
        try:
            con = sqlite3.connect('BOTDB.db')
            self.cur = con.cursor()
        except Exception:
            print("Couldn't connect to DataBase")
        tables = self.cur.execute('''SELECT name FROM sqlite_master WHERE type='table'
                              AND name='users';''').fetchall()
        if not tables:
            self.cur.execute('''CREATE TABLE users (id text, score integer, admin_point real))''')
        else:
            print("tables exist")

    def get_count(self):
        return self.count


if __name__ == '__main__':
    d = DataBaseAccess()
    print(d.get_count())
