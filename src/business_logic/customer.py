from .address import Address

class Customer:
    def __init__(self, address, first_name, last_name, email):
        self.address = address
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
