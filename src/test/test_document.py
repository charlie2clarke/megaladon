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


class Order:
    def __init__(self, order_id, customer, products):
        self.order_id = order_id
        self.customer = customer
        self.products = products


def setup_order(order_id, first_name, last_name, line_one, city, products):
    address = Address(line_one, city)
    customer = Customer(address, first_name, last_name)
    return Order(order_id, customer, products)


@pytest.fixture
def document():
    return Document()


address_label_test_data = [
    (1, "Test First Name", "Test Last Name", "Test Line One", "Test City",
     ["Test First Name Test Last Name", "Test Line One", "Test City"]),
]


@mock.patch('src.main.order_management.pdf.Pdf.write_address_label')
@pytest.mark.parametrize("order_id, first_name, last_name, line_one, city, expected", address_label_test_data)
def test_create_address_label(mock_pdf, document, order_id, first_name, last_name, line_one, city, expected):
    order = setup_order(order_id, first_name, last_name, line_one, city, None)
    address_label_contents = document.create_address_label(
        order)
    assert address_label_contents == expected


packaging_list_test_data = [
    (1, "Test First Name", "Test Last Name", "Test Line One", "Test Line Two", "Test City", [
     "Deliver To:", "Test First Name Test Last Name", "Test Line One", "Test City"])
]


@mock.patch('src.main.order_management.pdf.Pdf.write_address_label')
@pytest.mark.parametrize("order_id, first_name, last_name, line_one, city, expected", packaging_list_test_data)
def test_create_packaging_label(mock_pdf, document):
