'''Module to clear OnlineStore database.

Is not invoked by any of other modules in app and should be run as main.

Used during development and have added for completness.
'''
import os
import sqlite3
from sqlite3 import Error
from sqlite3.dbapi2 import Connection, Cursor


conn: Connection = sqlite3.connect(':memory:')
base_dir = os.path.dirname(__file__)
database_file = os.path.join(base_dir, 'OnlineStore.db')
conn = sqlite3.connect(database_file)
c: Cursor = conn.cursor()

c.execute('DROP TABLE IF EXISTS Address')
conn.commit()

c.execute('DROP TABLE IF EXISTS Customer')
conn.commit()

c.execute('DROP TABLE IF EXISTS Customer_Address')
conn.commit()

c.execute('DROP TABLE IF EXISTS Platform')
conn.commit()

c.execute('DROP TABLE IF EXISTS Postage')
conn.commit()

c.execute('DROP TABLE IF EXISTS Product')
conn.commit()

c.execute('DROP TABLE IF EXISTS Purchase')
conn.commit()

c.execute('DROP TABLE IF EXISTS Purchase_Product')
conn.commit()

c.execute('DROP TABLE IF EXISTS Status')
conn.commit()