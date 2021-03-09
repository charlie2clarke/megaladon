import sqlite3
import os
from sqlite3.dbapi2 import Connection, Cursor

class DataAccess:
    def __init__(self):
        self.conn = self.create_connection()
        self.cur = self.conn.cursor()
    
    def create_connection(self):
        # base_dir = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '/', 'database'))
        base_dir = os.path.join(os.path.dirname( __file__ ), 'database')
        database_file = os.path.join(base_dir, 'OnlineStore.db')
        return sqlite3.connect(database_file)

    def execute(self, query, data):
        if data is None:
            self.cur.execute(query)
        else:
            self.cur.execute(query, data)
        self.conn.commit()
        return self.cur
