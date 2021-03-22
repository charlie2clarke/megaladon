'''Module representing data held on a customer's address.

Is a composition of a customer.
'''


class Address:
    """A class to represent a customer address.

    A valid address will have all attributes with the line_two
    being an optional attribute.
    """

    def __init__(self, line_one, line_two, city, postcode):
        """Inits Address.

        Args:
            line_one: string of the first line of customer's address.
            line_two: string of the second line of customer's address.
            city: string of customer's city of residence.
            postcode: string of customer's postcode.
        """
        self._line_one = line_one
        self._line_two = line_two
        self._city = city
        self._postcode = postcode

    @property
    def line_one(self):
        '''String of first line to customer address.'''
        return self._line_one

    @property
    def line_two(self):
        '''String of second line to customer address'''
        return self._line_two

    @property
    def city(self):
        '''String of customer's city of residence.'''
        return self._city

    @property
    def postcode(self):
        '''String of customer's postcode.'''
        return self._postcode
