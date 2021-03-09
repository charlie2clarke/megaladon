from .order_controller import OrderController
from .pdf import Pdf

class PackagingList:
    def __init__(self):
        self.order_controller = OrderController(None)
        self.pdf = Pdf()
        self.orders_to_package = []

    def create_packaging_list(self, orders_selected):
        # date array, address array, items array
        for index, order in enumerate(orders_selected):
            order_number = int(order[0]) - 1
            order_obj = self.order_controller.orders['order_' + order[0]]

            date = order_obj.created_date

            address = ['Deliver To:', order_obj.customer.first_name + ' ' + order_obj.customer.last_name,
                       order_obj.customer.address.line_one, order_obj.customer.address.city]

            items = [[item['item'], item['quantity']]
                     for item in order_obj.product.ordered_items]

            items.insert(0, ['Item', 'Quantity'])

            self.pdf.write_packaging_list(date, address, items, order[0], index)


