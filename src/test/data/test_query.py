import os
import sqlite3
from sqlite3.dbapi2 import Connection, Cursor
import pytest
import mock
from src.main.order_management.data.query import Query

THIS_DIR = os.path.dirname(__file__)
TEST_DATABASE = os.path.join(THIS_DIR, 'database', 'TestOnlineStore.db')

class MockDataAccess:
    def __init__(self):
        self._conn = self._create_connection()
        self._cur = self._conn.cursor()
    
    def _create_connection(self):
        THIS_DIR = os.path.dirname(__file__)
        TEST_DATABASE = os.path.join(THIS_DIR, 'database', 'TestOnlineStore.db')
        return sqlite3.connect(TEST_DATABASE)

    def execute(self, query, data):
        if data is None:
            self._cur.execute(query)
        else:
            self._cur.execute(query, data)
        self._conn.commit()
        return self._cur

@pytest.fixture
def data_access():
    return MockDataAccess()

@pytest.fixture
def query():
    return Query()

@pytest.fixture
def setup_database(data_access):
    data_access.execute('''
        CREATE TABLE IF NOT EXISTS Address (
            id integer PRIMARY KEY AUTOINCREMENT,
            line_one text NOT NULL,
            line_two text,
            city text NOT NULL,
            postcode text
    );''', None)
    data_access.execute('''
        CREATE TABLE IF NOT EXISTS Customer (
            id integer PRIMARY KEY AUTOINCREMENT,
            first_name text NOT NULL,
            last_name text NOT NULL,
            email text
    );''', None)
    data_access.execute('''
        CREATE TABLE IF NOT EXISTS Customer_Address (
            customer_id integer,
            address_id integer,

            FOREIGN KEY (customer_id)
                REFERENCES Customer (id)
                    ON DELETE CASCADE
            FOREIGN KEY (address_id)
                REFERENCES Address (id)
                    ON DELETE CASCADE
            PRIMARY KEY (customer_id, address_id)
    );''', None)
    data_access.execute('''
        CREATE TABLE IF NOT EXISTS Platform (
            id integer PRIMARY KEY AUTOINCREMENT,
            platform_name integer NOT NULL,
            user_token text NOT NULL
    );''', None)
    data_access.execute('''
        CREATE TABLE IF NOT EXISTS Status (
            id integer PRIMARY KEY AUTOINCREMENT,
            status_description text NOT NULL
    );''', None)
    data_access.execute('''
        CREATE TABLE IF NOT EXISTS Postage (
            id integer PRIMARY KEY AUTOINCREMENT,
            postage_description text NOT NULL
    );''', None)
    data_access.execute('''
        CREATE TABLE IF NOT EXISTS Purchase (
            id integer PRIMARY KEY AUTOINCREMENT,
            platform_id integer,
            customer_id integer,
            status_id integer,
            postage_id integer,
            created_date text NOT NULL,
            dispatched_date text,
            completed_date text,
            
            FOREIGN KEY (platform_id)
                REFERENCES Platform (id)
                    ON DELETE CASCADE
            FOREIGN KEY (customer_id)
                REFERENCES Customer (id)
                    ON DELETE CASCADE
            FOREIGN KEY (status_id)
                REFERENCES Status (id)
                    ON DELETE CASCADE
    );''', None)
    data_access.execute('''
        CREATE TABLE IF NOT EXISTS Product (
            id integer PRIMARY KEY AUTOINCREMENT,
            product_name integer,
            product_description integer,
            individual_price real,
            stock_count integer,
            aisle integer,
            shelf integer
    );''', None)
    data_access.execute('''
        CREATE TABLE IF NOT EXISTS Purchase_Product (
            purchase_id integer,
            product_id integer,
            quantity integer,

            FOREIGN KEY (purchase_id)
                REFERENCES Purchase (id)
                    ON DELETE CASCADE
            FOREIGN KEY (product_id)
                REFERENCES Product (id)
                    ON DELETE CASCADE
            PRIMARY KEY (purchase_id, product_id)
    );''', None)
    
@pytest.fixture
def clean_database(data_access):
    data_access.execute('''DROP TABLE IF EXISTS Address''', None)
    data_access.execute('''DROP TABLE IF EXISTS Customer''', None)
    data_access.execute('''DROP TABLE IF EXISTS Customer_Address''', None)
    data_access.execute('''DROP TABLE IF EXISTS Platform''', None)
    data_access.execute('''DROP TABLE IF EXISTS Postage''', None)
    data_access.execute('''DROP TABLE IF EXISTS Product''', None)
    data_access.execute('''DROP TABLE IF EXISTS Purchase''', None)
    data_access.execute('''DROP TABLE IF EXISTS Purchase_Product''', None)
    data_access.execute('''DROP TABLE IF EXISTS Status''', None)
    

@pytest.fixture
def setup_test_data1(setup_database, data_access):
    data_access.execute('''
        INSERT INTO Address (line_one, line_two, city) 
            VALUES('Test Line One', 'Test Line Two', 'Test City')
    ''', None)
    data_access.execute('''
        INSERT INTO Customer (first_name, last_name, email) 
            VALUES('Test First Name', 'Test Last Name', 'Test Email')
    ''', None)
    data_access.execute('''
        INSERT INTO Customer_Address (customer_id, address_id)
            VALUES(1, 1)
    ''', None)
    data_access.execute('''
        INSERT INTO Postage (postage_description)
            VALUES('1st Class')
    ''', None)
    data_access.execute('''
        INSERT INTO Product (product_name, individual_price, stock_count, aisle, shelf)
            VALUES('Test Product', 100.00, 2, 3, 4)
    ''', None)
    data_access.execute('''
        INSERT INTO Status (status_description)
            VALUES('Awaiting')
    ''', None)
    data_access.execute('''
        INSERT INTO Purchase (customer_id, status_id, postage_id, created_date)
            VALUES(1, 1, 1, 'Date Now')
    ''', None)
    data_access.execute('''
        INSERT INTO Purchase_Product (purchase_id, product_id, quantity)
            VALUES(1, 1, 1)
    ''', None)

# @mock.patch('src.main.order_management.constants.DATABASE', return_value=TEST_DATABASE)
# def test_get_all_data(mock_data_access, query, clean_database, setup_database, setup_test_data1, data_access):
#     all_data = query.get_all_data()
#     assert all_data == ("jdi", "fmn")