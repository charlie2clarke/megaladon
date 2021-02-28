from .address import Address

class Customer:
    def __init__(self, address, first_name, last_name, email):
        self._address = address
        self._first_name = first_name
        self._last_name = last_name
        self._email = email

    @property
    def first_name(self):
        return self._first_name
    
    @property
    def last_name(self):
        return self._last_name

    @property
    def address(self):
        return self._address
