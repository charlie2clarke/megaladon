'''Tests Query class.

The Query class utilises the DataAccess class to abstract the connection
to an SQLite database. Therefore, I have created a MockDataAccess class
that inherits from DataAccess and have then pointed the connection to
my test database to not tamper with live database during testing.

Pytest fixtures have been used as a clean way of invoking functions for
setting up test database with required data. This means that in test functions
just by passing the function name as a parameter it is invoked.

The typical order for setting up test database
(and order fixtures are invoked):
1. clean database - clear existing tables and entries.
2. setup database - create database with required tables.
3. setup test data - populate test database with test data.
'''
import sqlite3
import pytest
import mock
from src.main.order_management.data.query import Query
from src.main.order_management.data.data_access import DataAccess
from src.test.test_config import TEST_DATABASE


class MockDataAccess(DataAccess):
    '''Creating a mock of DataAccess so that all behaviour is
    inherited and then can change the database connected to.
    '''
    def __init__(self):
        super(MockDataAccess, self).__init__()
        self._connection = self._create_connection()

    def _create_connection(self):
        return sqlite3.connect(TEST_DATABASE)


# Creating global instance rather than using pytest fixture
# so can use in return_value and only create one database connection.
# pytest fixtures create a new instance every time they are passed as
# a parameter.
mock_data_access = MockDataAccess()


@pytest.fixture
def query():
    return Query()


@pytest.fixture
def setup_database():
    # Creating tables in TestOnlineStore.
    mock_data_access.execute('''
        CREATE TABLE IF NOT EXISTS Address (
            id integer PRIMARY KEY AUTOINCREMENT,
            line_one text NOT NULL,
            line_two text,
            city text NOT NULL,
            postcode text
    );''', None)
    mock_data_access.execute('''
        CREATE TABLE IF NOT EXISTS Customer (
            id integer PRIMARY KEY AUTOINCREMENT,
            first_name text NOT NULL,
            last_name text NOT NULL,
            email text
    );''', None)
    mock_data_access.execute('''
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
    mock_data_access.execute('''
        CREATE TABLE IF NOT EXISTS Platform (
            id integer PRIMARY KEY AUTOINCREMENT,
            platform_name integer NOT NULL,
            user_token text NOT NULL
    );''', None)
    mock_data_access.execute('''
        CREATE TABLE IF NOT EXISTS Status (
            id integer PRIMARY KEY AUTOINCREMENT,
            status_description text NOT NULL
    );''', None)
    mock_data_access.execute('''
        CREATE TABLE IF NOT EXISTS Postage (
            id integer PRIMARY KEY AUTOINCREMENT,
            postage_description text NOT NULL
    );''', None)
    mock_data_access.execute('''
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
    mock_data_access.execute('''
        CREATE TABLE IF NOT EXISTS Product (
            id integer PRIMARY KEY AUTOINCREMENT,
            product_name integer,
            product_description integer,
            individual_price real,
            stock_count integer,
            aisle integer,
            shelf integer
    );''', None)
    mock_data_access.execute('''
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
def clean_database():
    # Deleting all tables and records in TestOnlineStore.
    mock_data_access.execute('''DROP TABLE IF EXISTS Address''', None)
    mock_data_access.execute('''DROP TABLE IF EXISTS Customer''', None)
    mock_data_access.execute('''DROP TABLE IF EXISTS Customer_Address''', None)
    mock_data_access.execute('''DROP TABLE IF EXISTS Platform''', None)
    mock_data_access.execute('''DROP TABLE IF EXISTS Postage''', None)
    mock_data_access.execute('''DROP TABLE IF EXISTS Product''', None)
    mock_data_access.execute('''DROP TABLE IF EXISTS Purchase''', None)
    mock_data_access.execute('''DROP TABLE IF EXISTS Purchase_Product''', None)
    mock_data_access.execute('''DROP TABLE IF EXISTS Status''', None)


@pytest.fixture
def setup_test_data1(setup_database):
    # Populating TestOnlineStore

    # Order entry 1:
    mock_data_access.execute('''
        INSERT INTO Address (line_one, line_two, city)
            VALUES('Test Line One', 'Test Line Two', 'Test City')
    ''', None)
    mock_data_access.execute('''
        INSERT INTO Customer (first_name, last_name, email)
            VALUES('Test First Name One', 'Test Last Name One', 'Test Email')
    ''', None)
    mock_data_access.execute('''
        INSERT INTO Customer_Address (customer_id, address_id)
            VALUES(1, 1)
    ''', None)
    mock_data_access.execute('''
        INSERT INTO Postage (postage_description)
            VALUES('1st Class')
    ''', None)
    mock_data_access.execute('''
        INSERT INTO Product (product_name, individual_price, stock_count,
                             aisle, shelf)
            VALUES('Test Product One', 100.00, 2, 3, 4)
    ''', None)
    mock_data_access.execute('''
        INSERT INTO Status (status_description)
            VALUES('Awaiting')
    ''', None)
    mock_data_access.execute('''
        INSERT INTO Purchase (customer_id, status_id, postage_id, created_date)
            VALUES(1, 1, 1, 'Date Now')
    ''', None)
    mock_data_access.execute('''
        INSERT INTO Purchase_Product (purchase_id, product_id, quantity)
            VALUES(1, 1, 1)
    ''', None)

    # Order entry 2:
    mock_data_access.execute('''
        INSERT INTO Address (line_one, line_two, city)
            VALUES('Test Line One', 'Test Line Two', 'Test City')
    ''', None)
    mock_data_access.execute('''
        INSERT INTO Customer (first_name, last_name, email)
            VALUES('Test First Name Two', 'Test Last Name Two', 'Test Email')
    ''', None)
    mock_data_access.execute('''
        INSERT INTO Customer_Address (customer_id, address_id)
            VALUES(2, 2)
    ''', None)
    mock_data_access.execute('''
        INSERT INTO Postage (postage_description)
            VALUES('2nd Class')
    ''', None)
    mock_data_access.execute('''
        INSERT INTO Product (product_name, individual_price, stock_count,
                             aisle, shelf)
            VALUES('Test Product Two', 100.00, 2, 4, 6)
    ''', None)
    mock_data_access.execute('''
        INSERT INTO Status (status_description)
            VALUES('Awaiting')
    ''', None)
    mock_data_access.execute('''
        INSERT INTO Purchase (customer_id, status_id, postage_id, created_date)
            VALUES(2, 1, 2, 'Date Now')
    ''', None)
    mock_data_access.execute('''
        INSERT INTO Purchase_Product (purchase_id, product_id, quantity)
            VALUES(2, 2, 1)
    ''', None)


@pytest.mark.happy
@mock.patch('src.main.order_management.data.query.DataAccess',
            return_value=mock_data_access)
def test_get_all_data(mock_data_access, clean_database,
                      setup_database, setup_test_data1):
    '''Test case to see if expected records are retrieved from main
    select query.
    '''
    query = Query()
    all_data = query.get_all_data()
    assert all_data == [
        (1,
         'Test Product One',
         1,
         'Test First Name One',
         'Test Last Name One',
         'Test Email',
         'Test Line One',
         'Test Line Two',
         'Test City',
         None,
         'Awaiting',
         'Date Now',
         None,
         None,
         '1st Class',
         100.0,
         1,
         3,
         4),

        (2,
         'Test Product Two',
         1,
         'Test First Name Two',
         'Test Last Name Two',
         'Test Email',
         'Test Line One',
         'Test Line Two',
         'Test City',
         None,
         'Awaiting',
         'Date Now',
         None,
         None,
         '2nd Class',
         100.0,
         2,
         4,
         6)
    ]


@pytest.mark.happy
@mock.patch('src.main.order_management.data.query.DataAccess',
            return_value=mock_data_access)
def test_get_new_data(mock_data_access, clean_database,
                      setup_database, setup_test_data1):
    '''Test case to see if only new records are retrieved.

    Should only return the second entry because am setting the order pointer
    (row index at which new records can be searched from) to 2.
    '''
    query = Query()
    query._new_order_pointer = 2
    new_data = query.get_new_data()
    assert new_data == [
        (2,
         'Test Product Two',
         1,
         'Test First Name Two',
         'Test Last Name Two',
         'Test Email',
         'Test Line One',
         'Test Line Two',
         'Test City',
         None,
         'Awaiting',
         'Date Now',
         None,
         None,
         '2nd Class',
         100.0,
         2,
         4,
         6)
    ]
