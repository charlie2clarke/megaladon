from .data_access import DataAccess

class Query:
    def __init__(self):
        self.data_access = DataAccess()
    
    def get_all_data(self):
        queryset = self.data_access.execute('''
            SELECT
                Purchase_Product.purchase_id,
                Product.product_name,
                Purchase_Product.quantity,
                Customer.first_name,
                Customer.last_name,
                Customer.email,
                Address.line_one,
                Address.line_two,
                Address.city,
                Address.postcode,
                Status.status_description,
                Purchase.created_date,
                Purchase.dispatched_date,
                Purchase.completed_date,
                Postage.postage_description,
                Product.individual_price,
                Product.id,
                Product.aisle,
                Product.shelf
            FROM
                Product
                INNER JOIN Purchase_Product ON Purchase_Product.product_id = Product.id
                INNER JOIN Purchase ON Purchase.id = Purchase_Product.purchase_id
                INNER JOIN Status ON Status.id = Purchase.status_id
                INNER JOIN Postage ON Postage.id = Purchase.postage_id
                INNER JOIN Customer ON Customer.id = Purchase.customer_id
                INNER JOIN Customer_Address ON Customer_Address.customer_id = Customer.id
                INNER JOIN Address ON Address.id = Customer_Address.address_id
            ORDER BY
                Purchase.id
        ''', None)
        return queryset.fetchall()