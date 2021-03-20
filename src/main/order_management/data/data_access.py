import sqlite3
from sqlite3.dbapi2 import Connection, Cursor
from ..constants import DATABASE

class DataAccess:
    def __init__(self):
        self._conn = self._create_connection()
        self._cur = self._conn.cursor()
    
    def _create_connection(self):
        return sqlite3.connect(DATABASE)

    def execute(self, query, data):
        if data is None:
            self._cur.execute(query)
        else:
            self._cur.execute(query, data)
        self._conn.commit()
        return self._cur
