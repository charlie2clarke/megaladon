from .initialise import Initialise
import asyncio


class Table:
    def __init__(self):
        self.initialise = Initialise()
        self.get_table_data()
        
    def get_table_data(self):
        # order number, customer, order date, status, total gross
        table_data = []
        order_number = 0

        for order in self.initialise.orders:
            order_number += 1
            row_data = []
            order_obj = self.initialise.orders[order]
            customer_name = order_obj.customer.first_name + ' ' + order_obj.customer.last_name

            row_data.append(str(order_number))
            row_data.append(customer_name)
            row_data.append(order_obj.created_date)
            row_data.append(order_obj.status)
            row_data.append('£' + str(order_obj.product.get_total(order_obj.product.ordered_items)))
            table_data.append(tuple(row_data))
        
        return table_data
