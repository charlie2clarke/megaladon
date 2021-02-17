import os
import sqlite3
from sqlite3 import Error
from sqlite3.dbapi2 import Connection, Cursor


conn : Connection = sqlite3.connect(':memory:')
base_dir = os.path.dirname( __file__ )
database_file = os.path.join(base_dir, 'OnlineStore.db')
conn = sqlite3.connect(database_file)
c : Cursor = conn.cursor()

# Populate Customer table
c.execute("""
    INSERT INTO Customer (first_name, last_name, email)
        VALUES ('john', 'smith', 'john.smith@gmail.com')  
""")
conn.commit()

# Populate Customer table
c.execute("""
    INSERT INTO Address (line_one, line_two, city, postcode)
        VALUES ('Summer Cottage Langley', 'Church Road', 'Exeter', 'EX1 802')  
""")
conn.commit()

# Populate Customer_Address table
c.execute("""
    INSERT INTO Customer_Address (customer_id, address_id)
        VALUES (1, 1)  
""")
conn.commit()

# Populate Platform table
c.execute("""
    INSERT INTO Platform (platform_name, user_token)
        VALUES ('eBay', 'abc123')  
""")
conn.commit()

# Populate Status table
c.execute("""
    INSERT INTO Status (status_description)
        VALUES ('Awaiting')  
""")
conn.commit()

# Populate Status table
c.execute("""
    INSERT INTO Status (status_description)
        VALUES ('Dispatched')  
""")
conn.commit()

# Populate Status table
c.execute("""
    INSERT INTO Status (status_description)
        VALUES ('Complete')  
""")
conn.commit()

# Populate Postage table
c.execute("""
    INSERT INTO Postage (postage_description)
        VALUES ('1st Class')  
""")
conn.commit()

# Populate Postage table
c.execute("""
    INSERT INTO Postage (postage_description)
        VALUES ('2nd Class')  
""")
conn.commit()

# Populate Product table
c.execute("""
    INSERT INTO Product (product_name, product_description, individual_price, stock_count, warehouse_location)
        VALUES ('Hat', 'Yellow crotched hat', 12.69, 4, 'aisle 1 shelf 2')  
""")
conn.commit()

# Populate Purchase table
c.execute("""
    INSERT INTO Purchase (platform_id, customer_id, status_id, postage_id, created_date)
        VALUES (1, 1, 1, 1, '18/02/2021')
""")
conn.commit()

# Populate Purchase_Product table
c.execute("""
    INSERT INTO Purchase_Product (purchase_id, product_id, quantity) 
        VALUES (1, 1, 1)
""")
conn.commit()
