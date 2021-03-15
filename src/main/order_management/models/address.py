"""
--------------------------------------------------------------------------------------------
title           : address.py
description     : Module representing data held on a customer's address
python_version  : 3.7.9
--------------------------------------------------------------------------------------------
"""

class Address:
    """
    A class to represent a customer address

    ...

    Attributes
    ----------
    line_one : string
        first line of address
    line_two : string
        second line of customer address
    city : string
        customer's city of residence
    postcode : string
        customer's postcode

    Methods
    -------
    create_address_label(orders_selected):
        Create strings to be output in pdf
    """
    def __init__(self, line_one, line_two, city, postcode):
        """
        Parameters
        ----------
        line_one : string
            first line of address
        line_two : string
            second line of customer address
        city : string
            customer's city of residence
        postcode : string
            customer's postcode
        """
        self._line_one = line_one
        self._line_two = line_two
        self._city = city
        self._postcode = postcode

    @property
    def line_one(self):
        return self._line_one

    @property
    def line_two(self):
        return self._line_two

    @property
    def city(self):
        return self._city

    @property
    def postcode(self):
        return self._postcode
