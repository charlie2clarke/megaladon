'''Abstracts SQLite database connection.

Used for executing queries to SQLite database.
'''
import sqlite3
from sqlite3.dbapi2 import Connection, Cursor
from ..constants import DATABASE


class DataAccess:
    '''A class to abstract SQLite database complexities.

    Query is the only module with a member variable to this class,
    so only one connection to database in held open.
    '''

    def __init__(self):
        '''Inits DataAccess.

        Creates connection to database with constant DATABASE file path.
        '''
        self._conn = self._create_connection()
        self._cur = self._conn.cursor()

    def _create_connection(self):
        return sqlite3.connect(DATABASE)

    def execute(self, query, data):
        '''Abstracts execute function to database.

        In all use cases query is needed to be committed
        so have implemented that here.

        Args:
            query: string SQL query to perform.
            data: a tuple of data referenced in SQL query with '?'.

        Returns:
            A tuple of rows retrieved from query.
        '''
        if data is None:
            self._cur.execute(query)
        else:
            self._cur.execute(query, data)
        self._conn.commit()
        return self._cur
