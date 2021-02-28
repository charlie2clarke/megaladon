from .order_controller import OrderController
from .order import Order
from .pdf import Pdf

class PickingList:
    def __init__(self):
        self.order_controller = OrderController()
        self.pdf = Pdf()
        self.ids = []
        self.product_descriptions = []
        self.quantities = []

    def create_picking_list(self):
        # product id, aisle, shelf, description, quantity, space for tick
        awaiting_orders = [order for order in self.order_controller.orders.values() if order.status == "Awaiting"]
        ordered_items = [product for order in awaiting_orders for product in order.product.ordered_items]
        ordered_items.sort(key=lambda product: (product['aisle'], product['shelf']))

        grouped_items = []
        grouped_items_position = -1
        # is assuming there are items to be picked

        for index, product in enumerate(ordered_items):
            previous = ordered_items[index-1]
            if index == 0:
                grouped_items.append(product)
                grouped_items_position += 1
            elif product['item_id'] == previous['item_id']:
                grouped_items[grouped_items_position]['quantity'] = \
                    grouped_items[grouped_items_position]['quantity'] + product['quantity']
            else:
                grouped_items.append(product)
                grouped_items_position += 1
        headers = list(grouped_items[0].keys())
        rows = [list(item.values()) for item in grouped_items]
        data = [headers] + rows
        self.pdf.write_picking_list(data)
            