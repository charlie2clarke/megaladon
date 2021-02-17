import os
import sqlite3
from sqlite3 import Error
from sqlite3.dbapi2 import Connection, Cursor


def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn : Connection = sqlite3.connect(':memory:')
        conn = sqlite3.connect(db_file)      
        return conn
    except Error:
        print(Error)

    return conn


def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
        conn.commit()
    except Error:
        print(Error)


def main():
    base_dir = os.path.dirname(__file__)
    database = os.path.join(base_dir, 'OnlineStore.db')

    # Have created a separate table for addresses, because it is possible for
    # customers to have more than one registered address
    sql_create_address_table = """ CREATE TABLE IF NOT EXISTS Address (
                                        id integer PRIMARY KEY AUTOINCREMENT,
                                        line_one text NOT NULL,
                                        line_two text,
                                        city text NOT NULL,
                                        postcode text NOT NULL
                                    );"""

    sql_create_customer_table = """ CREATE TABLE IF NOT EXISTS Customer (
                                        id integer PRIMARY KEY AUTOINCREMENT,
                                        first_name text NOT NULL,
                                        last_name text NOT NULL,
                                        email text NOT NULL
                                    );"""

    sql_create_customer_address_table = """ CREATE TABLE IF NOT EXISTS Customer_Address (
                                                customer_id integer,
                                                address_id integer,

                                                FOREIGN KEY (customer_id)
                                                    REFERENCES Customer (id)
                                                        ON DELETE CASCADE
                                                FOREIGN KEY (address_id)
                                                    REFERENCES Address (id)
                                                        ON DELETE CASCADE
                                                PRIMARY KEY (customer_id, address_id)
                                            );"""

    sql_create_platform_table = """ CREATE TABLE IF NOT EXISTS Platform (
                                        id integer PRIMARY KEY AUTOINCREMENT,
                                        platform_name integer NOT NULL,
                                        user_token text NOT NULL
                                );"""

    sql_create_status_table = """ CREATE TABLE IF NOT EXISTS Status (
                                    id integer PRIMARY KEY AUTOINCREMENT,
                                    status_description text NOT NULL
                                    );"""

    sql_create_postage_table = """ CREATE TABLE IF NOT EXISTS Postage (
                                    id integer PRIMARY KEY AUTOINCREMENT,
                                    postage_description text NOT NULL
                                    );"""

    sql_create_purchase_table = """ CREATE TABLE IF NOT EXISTS Purchase (
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
                                );"""
                            
    sql_create_product_table = """ CREATE TABLE IF NOT EXISTS Product (
                                    id integer PRIMARY KEY AUTOINCREMENT,
                                    product_name integer,
                                    product_description integer,
                                    individual_price real,
                                    stock_count integer,
                                    warehouse_location text
                                    );"""

    sql_create_purchase_product_table = """ CREATE TABLE IF NOT EXISTS Purchase_Product (
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
                                    );"""
              

    # create a database connection
    conn = create_connection(database)

    # create tables
    if conn is not None:
        conn.execute("PRAGMA foreign_keys = ON")
        # create projects table
        create_table(conn, sql_create_address_table)
        
        # create customer table
        create_table(conn, sql_create_customer_table)

        # create customer_address table
        create_table(conn, sql_create_customer_address_table)

        # create platform table
        create_table(conn, sql_create_platform_table)

        # create status table
        create_table(conn, sql_create_status_table)

        # create postage table
        create_table(conn, sql_create_postage_table)

        # create purchase table
        create_table(conn, sql_create_purchase_table)

        # create product table
        create_table(conn, sql_create_product_table)

        # create purchase_product table
        create_table(conn, sql_create_purchase_product_table)

    else:
        print("Error! cannot create the database connection.")


if __name__ == '__main__':
    main()
