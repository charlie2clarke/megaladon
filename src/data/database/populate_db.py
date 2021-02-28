import os
import sqlite3
from sqlite3 import Error
from sqlite3.dbapi2 import Connection, Cursor


conn : Connection = sqlite3.connect(':memory:')
base_dir = os.path.dirname( __file__ )
database_file = os.path.join(base_dir, 'OnlineStore.db')
conn = sqlite3.connect(database_file)
c : Cursor = conn.cursor()


# # Populate Customer table
# c.execute("""
#     INSERT INTO Customer (first_name, last_name)
#         VALUES ('George', 'Clooney')  
# """)
# conn.commit()

# # Populate Address table
# c.execute("""
#     INSERT INTO Address (line_one, city)
#         VALUES ('98 Prospect Park', 'Newcastle')  
# """)
# conn.commit()

# # Populate Address table
# c.execute("""
#     INSERT INTO Customer_Address (customer_id, address_id)
#         VALUES (1, 1)  
# """)
# conn.commit()


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
    INSERT INTO Product (product_name, individual_price, stock_count, aisle, shelf)
        VALUES ('Samsung Galaxy S21 Ultra', 799.00, 20, 3, 3)  
""")
conn.commit()

# Populate Product table
c.execute("""
    INSERT INTO Product (product_name, individual_price, stock_count, aisle, shelf)
        VALUES ('OnePlus 8 Pro', 429.00, 20, 3, 4)  
""")
conn.commit()

# Populate Product table
c.execute("""
    INSERT INTO Product (product_name, individual_price, stock_count, aisle, shelf)
        VALUES ('iPhone 12', 1299.00, 20, 3, 5)  
""")
conn.commit()

# Populate Product table
c.execute("""
    INSERT INTO Product (product_name, individual_price, stock_count, aisle, shelf)
        VALUES ('Oppo Find X2 Pro', 899.00, 20, 3, 6)  
""")
conn.commit()

# Populate Product table
c.execute("""
    INSERT INTO Product (product_name, individual_price, stock_count, aisle, shelf)
        VALUES ('Motorola Edge Plus', 300.00, 20, 3, 7)  
""")
conn.commit()

# Populate Product table
c.execute("""
    INSERT INTO Product (product_name, individual_price, stock_count, aisle, shelf)
        VALUES ('Xiaomi Mi Note 10', 250.00, 20, 3, 8)  
""")
conn.commit()

# Populate Product table
c.execute("""
    INSERT INTO Product (product_name, individual_price, stock_count, aisle, shelf)
        VALUES ('Sony Xperia 1', 479.00, 20, 3, 9)  
""")
conn.commit()

# Populate Product table
c.execute("""
    INSERT INTO Product (product_name, individual_price, stock_count, aisle, shelf)
        VALUES ('Nokia 3310', 39.00, 20, 4, 2)  
""")
conn.commit()
