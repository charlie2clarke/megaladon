import sqlite3
import os
from sqlite3.dbapi2 import Connection, Cursor

class DataAccess:
    def __init__(self):
        self.conn = self.create_connection()
        self.cur = self.conn.cursor()
    
    def create_connection(self):
        base_dir = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'database'))
        database_file = os.path.join(base_dir, 'OnlineStore.db')
        return sqlite3.connect(database_file)

    def execute(self, query, data):
        if data is None:
            self.cur.execute(query)
        else:
            self.cur.execute(query, data)
        self.conn.commit()
        return self.cur

    def authorise_user(self, username, password):
        if self.check_if_exists(username):
            if self.validate_password(username, password):
                return True, "valid"
            else:
                return False, "incorrect password"
        else:
            return False, "incorrect username"

    def check_if_exists(self, username):
        data = self.execute("SELECT user_id FROM user WHERE username = ?", (username,))
        data = data.fetchone()
        if data is None:
            print("There is no username " + username)
            return False
        else:
            print("Username " + username + ' exists')
            return True

    def validate_password(self, username, password):
        data = self.execute("SELECT password FROM user WHERE username = ?", (username,))
        data = data.fetchone()
        print(data)
        if data is not None:
            print(data[0])
            if data[0] == password:
                print("Correct password " + password)
                return True
        else:
            print("Incorrect password for the username " + username)
            return False

    # def insert_to_database(self, username, password):
    #     # conn : Connection = sqlite3.connect(':memory:')
    #     # conn = sqlite3.connect('kivy_db.db')
    #     # c : Cursor = conn.cursor()

    #     # user_details = (username, password)
    #     self.execute("INSERT INTO user (username, password) VALUES (?, ?)", (username, password))

    #     conn.commit()
    #     c.close()