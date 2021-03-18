import pytest
import mock
from src.main.order_management.document import Document


class Address:
    def __init__(self, line_one, city):
        self.line_one = line_one
        self.city = city


class Customer:
    def __init__(self, address, first_name, last_name):
        self.address = address
        self.first_name = first_name
        self.last_name = last_name


class Product:
    def __init__(self, product_id, product_name, price, aisle, shelf):
        self.product_id = product_id
        self.product_name = product_name
        self.price = price
        self.aisle = aisle
        self.shelf = shelf


class Order:
    def __init__(self, order_id, customer, products, created_date, status):
        self.order_id = order_id
        self.customer = customer
        self.products = products
        self.created_date = created_date
        self.status = status


def setup_order(order_id, first_name, last_name, line_one, city, products, status):
    address = Address(line_one, city)
    customer = Customer(address, first_name, last_name)
    if products is not None:
        products = [Product(*product) for product in products]
    return Order(order_id, customer, products, None, status)


@pytest.fixture
def document():
    return Document()


picking_list_products = [[1, 'Test Product One', 99.99, 1, 2], [1, 'Test Product One', 99.99, 1, 2], [
    2, 'Test Product Two', 11.11, 2, 4], [3, 'Test Product Three', 22.22, 1, 1]]
picking_list_orders = [setup_order(
    1, "Test First Name", "Test Last Name", "Test Line One", "Test City", picking_list_products, "Awaiting")]
picking_list_expected = [["Product ID", "Product Name", "Quantity", "Individual Price", "Aisle", "Shelf"], [
    3, "Test Product Three", 1, 22.22, 1, 1], [1, "Test Product One", 2, 99.99, 1, 2], [2, 'Test Product Two', 1, 11.11, 2, 4]]
picking_list_data = [
    (picking_list_orders, picking_list_expected)
]

@mock.patch('src.main.order_management.pdf.Pdf.write_picking_list')
@pytest.mark.parametrize("picking_list_orders, expected", picking_list_data)
def test_create_picking_list(mock_pdf, document, picking_list_orders, expected):
    picking_list_contents = document.create_picking_list(picking_list_orders)
    assert picking_list_contents == expected



packaging_list_products_and_quantities = {
    'Test Product 1': 2, 'Test Product 2': 4}
packaging_list_order = setup_order(
    1, "Test First Name", "Test Last Name", "Test Line One", "Test City", None, None)
packaging_list_test_data = [
    (packaging_list_order, packaging_list_products_and_quantities, ([
     "Deliver To:", "Test First Name Test Last Name", "Test Line One", "Test City"], [['Item', 'Quantity'], ['Test Product 1', 2], ['Test Product 2', 4]]))
]


@mock.patch('src.main.order_management.pdf.Pdf.write_packaging_list')
@pytest.mark.parametrize("packaging_list_order, packaging_list_products_and_quantities, expected", packaging_list_test_data)
def test_create_packaging_label(mock_pdf, document, packaging_list_order, packaging_list_products_and_quantities, expected):
    packaging_list_contents = document.create_packaging_list(
        packaging_list_order, packaging_list_products_and_quantities)
    assert packaging_list_contents == expected


address_label_order = setup_order(
    1, "Test First Name", "Test Last Name", "Test Line One", "Test City", None, None)
address_label_test_data = [
    (address_label_order, [
     "Test First Name Test Last Name", "Test Line One", "Test City"]),
]


@mock.patch('src.main.order_management.pdf.Pdf.write_address_label')
@pytest.mark.parametrize("address_label_order, expected", address_label_test_data)
def test_create_address_label(mock_pdf, document, address_label_order, expected):
    # order = setup_order(order_id, first_name, last_name, line_one, city, None)
    address_label_contents = document.create_address_label(
        address_label_order)
    assert address_label_contents == expected
