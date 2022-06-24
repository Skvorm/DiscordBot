import os
import sqlite3
from sqlite3 import Error


class DataBaseAccess:
    cur = ""
    con = ""

    # get user
    # put user
    # get user_score
    # put user_score (increment,set)
    def __init__(self):
        try:
            self.con = sqlite3.connect('BOTDB.db')
            self.cur = self.con.cursor()
        except Exception:
            print("Couldn't connect to DataBase")
        tables = self.cur.execute('''SELECT name FROM sqlite_master WHERE type='table'
                              AND name='users';''').fetchall()
        if not tables:
            self.cur.execute('''CREATE TABLE users (id int PRIMARY KEY, score integer, admin_point 
            real)''')
        else:
            # print("tables exist")
            pass

    def put_user(self, user=[0, 0, 0]):
        try:
            query = '''INSERT INTO users VALUES (?,?,?)'''
            self.cur.execute(query, user)
            self.con.commit()
            return True
        except Error as e:
            # print("couldn't Insert User")
            return False
    def get_user(self,user_id):
            try:
                query = '''Select * from users where id=?'''
                user=self.cur.execute(query, str(user_id)).fetchone()
                return user
            except Error as e:
                # print("couldn't Insert User")
                return [-1,0,0]


if __name__ == '__main__':
    d = DataBaseAccess()
    # print(d.get_count())
    #print(d.put_user([1,2,0]))
    #print(d.get_user(1))
