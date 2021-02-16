from data.data_access.data_access import DataAccess

class Order:
    def __init__(self):
        self.data_access = DataAccess()

    def get_order_table_data(self):
        # Item, Quantity, Customer Name, Status
        queryset = self.data_access.execute('''
            SELECT
                Product.product_name, 
                Purchase_Product.quantity, 
                Customer.first_name, 
                Customer.last_name, 
                Status.status_description
            FROM
                Product
                INNER JOIN Purchase_Product ON Purchase_Product.product_id = Product.id
                INNER JOIN Purchase ON Purchase.id = Purchase_Product.purchase_id
                INNER JOIN Customer ON Customer.id = Purchase.customer_id
                INNER JOIN Status ON Status.id = Purchase.status_id
        ''', None)
        return queryset.fetchall()

