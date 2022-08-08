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
            self.cur.execute('''CREATE TABLE users (id int PRIMARY KEY, score integer)''')
        else:
            # print("tables exist")
            pass

    def put_user(self, user=None):
        if user is None:
            user = [0, 0]
        try:
            query = '''INSERT INTO users VALUES (?,?)'''
            self.cur.execute(query, user)
            self.con.commit()
            return True
        except Error as e:
            # print("couldn't Insert User")
            return False

    def get_user(self, user_id):
        try:
            query = '''Select * from users where id=?'''
            user = self.cur.execute(query, str(user_id)).fetchone()
            return user
        except Error as e:
            # print("couldn't Insert User")
            return [-1, 0]

    def get_user_score(self, user_id):
        try:
            query = '''Select score from users where id=?'''
            user_score = self.cur.execute(query, str(user_id)).fetchone()
            if user_score:
                return user_score[0]
            else:
                return None
        except Error as e:
            print(f"{e} couldn't get score")
            return None

    # def set_user_score(self,user_id,score):
    def set_user_score(self, user_id, score):
        try:
            query = '''Update users SET score=? WHERE  id=?'''
            user_score = self.cur.execute(query, [score, str(user_id)])
            return True
        except Error as e:
            print(f"{e} couldn't set score")
            return False

    def increment_user_score(self, user_id, amount):
        try:
            user_score = self.get_user_score(user_id)
            if user_score:
                user_score += amount
            else:
                return False
            query = '''Update users SET score=? WHERE  id=?'''
            fin_score = self.cur.execute(query, [user_score, str(user_id)])
            return True
        except Error as e:
            print(f"{e}:couldn't increment score")
            return False

    def clear_user_table(self):
        try:
            query = '''DELETE FROM users'''
            self.cur.execute(query)
            return True
        except sqlite3.Error:
            print("couldn't clear table")
            return False


if __name__ == '__main__':
    d = DataBaseAccess()
    # print(d.put_user([1,2]))
    # print(d.put_user([1,1]))
    # print(d.put_user([2,1]))
    #print(d.get_user_score(1))
    #print(d.set_user_score(1, 50))
    #print(d.increment_user_score(1, 25))
    #print(d.increment_user_score(3, 25))
    #print(d.get_user_score(3))
    print(f'clearing table:{d.clear_user_table()}')
    d.con.commit()
