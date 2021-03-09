"""
--------------------------------------------------------------------------------------------
title           : address_label.py
description     : Formats order data for creation of address labels in the pdf.py module.
python_version  : 3.7.9
--------------------------------------------------------------------------------------------
"""

from .order_controller import OrderController
from .pdf import Pdf


class AddressLabel:
    """
    A class for formatting data to be input into address label pdf.

    ...

    Attributes
    ----------
    order_controller : OrderController
        member variable to access order instances
    pdf : Pdf
        member variable to invoke writing of pdf

    Methods
    -------
    create_address_label(orders_selected):
        Create strings to be output in pdf
    """

    def __init__(self):
        """
        Constructs all the necessary attributes for the AddressLabel object.
        """
        self._order_controller = OrderController(None)
        self._pdf = Pdf()

    def create_address_label(self, orders_selected):
        """
            For each of the orders selected with checkboxes will find the data for that order
            and format is suitable for the pdf module.
         
            Parameters:
                orders_selected: an array of the row data from each row checked with a checkbox
                (each item is a string).
        """
        for index, order in enumerate(orders_selected):
            order_id = int(order[0]) - 1
            order_obj = self._order_controller.orders['order_' + order[0]]

            address = [order_obj.customer.first_name + ' ' + order_obj.customer.last_name,
                       order_obj.customer.address.line_one, order_obj.customer.address.city]

            self._pdf.write_address_label(address, order_id, index)
