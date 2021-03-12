"""
--------------------------------------------------------------------------------------------
title           : address_label.py
description     : Formats order data for creation of address labels in the pdf.py module.
python_version  : 3.7.9
--------------------------------------------------------------------------------------------
"""
from pdf import Pdf
from constants import ADDRESS_LABELS_DIR, PACKAGING_LIST_DIR, PICKING_LIST_DIR


class Document:
    def __init__(self):
        self._pdf = Pdf()

    def _format_address(self, order):
        return [order.customer.first_name + ' ' + order.customer.last_name,
                    order.customer.address.line_one, order.customer.address.city]

    def create_picking_list(self, orders):
        awaiting_orders = [order for order in orders.values() if order.status == "Awaiting"]
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
        picking_table_data = [headers] + rows
        self._pdf.write_picking_list(picking_table_data, PICKING_LIST_DIR)

    def create_packaging_list(self, order):
        # date array, address array, items array
        address = self._format_address(order)
        address.insert(0, 'Deliver To:')
        items = [[item['item'], item['quantity']]
                    for item in order.product.ordered_items]
        items.insert(0, ['Item', 'Quantity'])
        
        self._pdf.write_packaging_list(order.created_date, address, items, order.order_id, PACKAGING_LIST_DIR)

    def create_address_label(self, order):        
        address = self._format_address(order)
        self._pdf.write_address_label(address, order.order_id, ADDRESS_LABELS_DIR)
