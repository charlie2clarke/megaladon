'''Represents data stored on customer.

Is a composition of an order.
'''


class Customer:
    '''A class to represent a customer.'''

    def __init__(self, address, first_name, last_name, email):
        '''Inits Customer.

        Args:
            address: instance of Address inherent to the customer.
            first_name: string of customer first name.
            last_name: string of customer last name.
            email: string of customer email.
        '''
        self._address = address
        self._first_name = first_name
        self._last_name = last_name
        self._email = email

    @property
    def first_name(self):
        '''String of customer's first name.'''
        return self._first_name

    @property
    def last_name(self):
        '''String of customer's last name.'''
        return self._last_name

    @property
    def address(self):
        '''Instance of Address inherent to customer.'''
        return self._address

    @property
    def email(self):
        '''String of customer's email.'''
        return self._email
