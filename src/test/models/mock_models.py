'''Creating mock base classes using inheritance.

This implementation means that the actual/main classes
aren't instantiated. Inheritance has been used to keep
methods and attributes from original classes so that
instances created are a true reflection of the base ones.
'''
from src.main.order_management.models.order import Order
from src.main.order_management.models.product import Product
from src.main.order_management.models.customer import Customer
from src.main.order_management.models.address import Address


class MockAddress(Address):
    pass


class MockCustomer(Customer):
    pass


class MockOrder(Order):
    pass


class MockProduct(Product):
    pass


class MockOrder(Order):
    pass


def setup_order(order_id,
                first_name,
                last_name,
                email,
                line_one,
                city,
                products,
                status,
                dispatched_date):
    '''Helper function to create instances of mock models.

    Only includes parameters that have been necessary for tests.
    '''
    address = MockAddress(line_one, None, city, None)
    customer = MockCustomer(address, first_name, last_name, email)
    if products is not None:
        products = [MockProduct(*product) for product in products]
    return MockOrder(order_id, products, customer, status, "Date Now",
                     dispatched_date, None, "1st Class")
