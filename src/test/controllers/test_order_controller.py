import pytest
import mock
from datetime import datetime
from src.main.order_management.controllers.order_controller import OrderController


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
        self.dispatched_date = None
        self.completed_date = None
        self.status = status

    def __eq__(self, other):
        return self.customer.first_name == other.customer.first_name


def setup_order(order_id, first_name, last_name, line_one, city, products, status):
    address = Address(line_one, city)
    customer = Customer(address, first_name, last_name)
    if products is not None:
        products = [Product(*product) for product in products]
    return Order(order_id, customer, products, "Test Date", status)


@pytest.fixture
def order_controller():
    return OrderController()

pytest.order_one = setup_order(1, 'Test First Name', 'Test Last Name', 'Test Line One', 'Test City', [
[1, 'Test Product One', 99.99, 1, 2], [1, 'Test Product One', 99.99, 1, 2], [2, 'Test Product Two', 18.18, 2, 2]], "Awaiting")

get_total_products_one = [[1, 'Test Product One', 99.99, 1, 2], [1, 'Test Product One', 99.99, 1, 2], [
    2, 'Test Product Two', 11.11, 2, 4], [3, 'Test Product Three', 22.22, 1, 1]]
get_total_order_one = setup_order(
    1, None, None, None, None, get_total_products_one, None)
get_total_products_two = [[1, 'Test Product One', -5, 1, 2], [1, 'Test Product One', 2, 1, 2], [
    2, 'Test Product Two', 2.999, 2, 4], [3, 'Test Product Three', 4.00, 1, 1]]
get_total_order_two = setup_order(
    1, None, None, None, None, get_total_products_two, None)
get_total_test_data = [
    (get_total_order_one.products, 233.30999999999997),
    (get_total_order_two.products, 3.999)
]


@pytest.mark.parametrize("order, expected", get_total_test_data)
def test__get_total_price(order_controller, order, expected):
    total_price = order_controller._get_total_price(order)
    assert total_price == expected


get_product_quantities_test_data = [
    (pytest.order_one, {'Test Product One': 2, 'Test Product Two': 1})
]


@pytest.mark.parametrize("order, expected", get_product_quantities_test_data)
def test_get_product_quantities(order_controller, order, expected):
    products_and_quantities = order_controller.get_product_quantities(order)
    assert products_and_quantities == expected


def test_initialise_orders(order_controller):
    initialise_orders_test_data = [
        (1, 'Oppo Find X2 Pro', 1, 'George', 'Clooney', 'george.clooney@gmail.com', '98 Prospect Park', None, 'Newcastle', None, 'Awaiting', '2021-03-16', None, None, "2nd Class", 899.0, 4, 4, 6), 
        (2, 'Samsung Galaxy S21 Ultra', 1, 'Jennifer', 'Lawrence', 'jennifer.lawrence@gmail.com', '25 Landsdowne Terrace', None, 'York', None, 'Awaiting', '2021-03-16', None, None, "2nd Class", 799.0, 1, 1, 3),
        (2, 'iPhone 12', 1, 'Jennifer', 'Lawrence', 'jennifer.lawrence@gmail.com', '25 Landsdowne Terrace', None, 'York', None, 'Awaiting', '2021-03-16', None, None, "2nd Class", 1299.0, 3, 2, 5),
        (3, 'OnePlus 8 Pro', 2, 'Nicole', 'Kidman', 'nicole.kidman@gmail.com', '15 Prospect Park', None, 'Exeter', None, 'Awaiting', '2021-03-16', None, None, '2nd Class', 429.0, 2, 3, 4)
    ]
    expected = {
        'order_1': setup_order(1, 'George', 'Clooney', '98 Prospect Park', 'Newcastle', [[4, 'Oppo Find X2 Pro', 899.0, 4, 6]], 'Awaiting'),
        'order_2': setup_order(2, 'Jennifer', 'Lawrence', '25 Landsdowne Terrace', 'York', [[1, 'Samsung Galaxy S21 Ultra', 799.0, 1, 3], [3, 'iPhone 12', 1299.0, 2, 5]], 'Awaiting'),
        'order_3': setup_order(3, 'Nicole', 'Kidman', '15 Prospect Park', 'Exeter', [[2, 'OnePlus 8 Pro', 429.0, 3, 4]], 'Awaiting')
    }
    initialised_orders = order_controller.initialise_orders(initialise_orders_test_data)
    assert initialised_orders['order_1'].customer.first_name == expected['order_1'].customer.first_name
    assert initialised_orders['order_2'].customer.first_name == expected['order_2'].customer.first_name
    assert initialised_orders['order_3'].customer.first_name == expected['order_3'].customer.first_name
    # for test_order in initialised_orders:
    #     test_order_obj = initialised_orders[test_order]
    #     for expected_order in expected:
    #         expected_order_obj = expected[expected_order]
    #         assert test_order_obj == expected_order_obj


@mock.patch('src.main.order_management.controllers.order_controller.OrderController._get_total_price', return_value=99)
@pytest.mark.parametrize("expected", [[("1", "Test First Name Test Last Name", "Test Date", "Awaiting", "£99")]])
def test_get_table_data(mock__get_total_price, order_controller, expected):
    order_controller._orders = {'order_1': pytest.order_one}
    table_data = order_controller.get_table_data()
    assert table_data == expected


get_order_details_test_data = [
    ("1", ("Order number 1", "Customer: Test First Name Test Last Name,\n\nOrdered items:\n  Test Product One * 2\n  Test Product Two * 1\n\nOrder date: Test Date\n\nDispatched date: None\n\nCompleted date: None"))
]

@mock.patch('src.main.order_management.controllers.order_controller.OrderController.get_product_quantities', return_value={"Test Product One": 2, "Test Product Two": 1})
@pytest.mark.parametrize("order_id, expected", get_order_details_test_data)
def test_get_order_details(mock_get_product_quantities, order_controller, order_id, expected):
    order_controller._orders = {'order_1': pytest.order_one}
    order_details = order_controller.get_order_details(order_id)
    assert order_details == expected

def get_expected_order():
    expected_order = setup_order(1, 'Test First Name', 'Test Last Name', 'Test Line One', 'Test City', [
    [1, 'Test Product One', 99.99, 1, 2], [1, 'Test Product One', 99.99, 1, 2], [2, 'Test Product Two', 18.18, 2, 2]], "Dispatched")
    expected_order.dispatched_date = "Date Now"
    return expected_order


@mock.patch("src.main.order_management.outlook_email.update_status")
@pytest.mark.parametrize("order, expected", [(['1', None, None, 'Awaiting'], [{'order_1': get_expected_order()}])])
def test_update_order_status(mock_email, order_controller, order, expected):
    order_controller._orders = {'order_1': pytest.order_one}
    updated_order = order_controller.update_order_status(order)
    assert updated_order.status == expected[0]['order_1'].status
