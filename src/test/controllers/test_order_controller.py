'''Tests OrderController - the methods manipulating Order instances.

All paths in methods are considered happy because validation would've
been carried out prior to invoking, although edge cases have been tested
as summarised in method comments.
'''
import pytest
import mock
from unittest.mock import Mock
from datetime import datetime
from src.test.models.mock_models import (
                                MockAddress,
                                MockCustomer,
                                MockProduct,
                                MockOrder,
                                setup_order)

from src.main.order_management.controllers.order_controller \
    import OrderController


@pytest.fixture
def order_controller():
    return OrderController()


pytest.order_one = setup_order(1, 'Test First Name', 'Test Last Name',
                               'testemailone@something.com', 'Test Line One',
                               'Test City',
                               [[1, 'Test Product One', 99.99, 1, 2],
                                [1, 'Test Product One', 99.99, 1, 2],
                                [2, 'Test Product Two', 11.11, 2, 4],
                                [3, 'Test Product Three', 22.22, 1, 1]],
                               "Awaiting", None)

# Edge case test with prices in non-expected format - could be the case
# if input into database incorrectly, or depedandant on how discounts are
# handled.
pytest.order_two = setup_order(1, 'Test First Name', 'Test Last Name',
                               'testemailtwo@something.com', 'Test Line One',
                               'Test City',
                               [[1, 'Test Product One', -5, 1, 2],
                                [1, 'Test Product One', 2, 1, 2],
                                [2, 'Test Product Two', 2.999, 2, 4],
                                [3, 'Test Product Three', 4.00, 1, 1],
                                [2, 'Test Product Two', 2.999, 2, 4]],
                               "Dispatched", "Test Date")


@pytest.mark.happy
@pytest.mark.parametrize("order, expected", [
    (pytest.order_one.products, 233.30999999999997),
    (pytest.order_two.products, 6.998)
])
def test_get_total_price(order_controller, order, expected):
    '''Test case for getting total price for a given order.

    Function only has a happy path, but includes the first test order
    with usual format of item prices.

    Second test case includes products with non-expected units of price.
    I.e. to more than two d.p. and a minus.
    '''
    total_price = order_controller.get_total_price(order)
    assert total_price == expected


@pytest.mark.happy
@pytest.mark.parametrize("order, expected", [
    (pytest.order_one, {'Test Product One': 2, 'Test Product Three': 1,
                        'Test Product Two': 1}),
    (pytest.order_two, {'Test Product One': 2, 'Test Product Three': 1,
                        'Test Product Two': 2})
])
def test_get_product_quantities(order_controller, order, expected):
    '''Test case for finding the all products and quantities for a given order.

    Function only contains a happy path but has included a test for
    the first order with a usual sequential list of orders.

    The second test case/order had orders non-sequentially to be
    sure that this doesn't impact the items and quantities returned.
    '''
    products_and_quantities = order_controller.get_product_quantities(order)
    assert products_and_quantities == expected


@pytest.mark.happy
def test_initialise_orders(order_controller):
    '''Test cases for method instantiating Order.

    Test data includes first scenario for a customer with a single item
    in order.

    Second order/scenario has a customer with multiple of the same item
    ordered.

    Third order/scenario has a customer with multiple different items in
    order.

    Scenario of no orders isn't possible because of logic in Main.
    '''
    initialise_orders_test_data = [
        (1, 'Oppo Find X2 Pro', 1, 'George', 'Clooney',
         'george.clooney@gmail.com', '98 Prospect Park', None, 'Newcastle',
         None, 'Awaiting', '2021-03-16', None, None, "2nd Class", 899.0, 4,
         4, 6),
        (2, 'Samsung Galaxy S21 Ultra', 1, 'Jennifer', 'Lawrence',
         'jennifer.lawrence@gmail.com', '25 Landsdowne Terrace', None, 'York',
         None, 'Awaiting', '2021-03-16', None, None, "2nd Class", 799.0, 1,
         1, 3),
        (2, 'iPhone 12', 1, 'Jennifer', 'Lawrence',
         'jennifer.lawrence@gmail.com', '25 Landsdowne Terrace', None, 'York',
         None, 'Awaiting', '2021-03-16', None, None, "2nd Class", 1299.0, 3,
         2, 5),
        (3, 'OnePlus 8 Pro', 2, 'Nicole', 'Kidman',
         'nicole.kidman@gmail.com', '15 Prospect Park', None, 'Exeter', None,
         'Awaiting', '2021-03-16', None, None, '2nd Class', 429.0, 2,
         3, 4)
    ]
    initialised_orders = order_controller.initialise_orders(
        initialise_orders_test_data)

    for test_order in initialised_orders:
        test_order_obj = initialised_orders[test_order]
        if test_order == "order_1":
            assert test_order_obj.customer.first_name == "George"
            assert test_order_obj.customer.last_name == "Clooney"
            assert len(test_order_obj.products) == 1
            assert test_order_obj.products[0].product_name == \
                "Oppo Find X2 Pro"
        elif test_order == "order_2":
            assert test_order_obj.customer.first_name == "Jennifer"
            assert test_order_obj.customer.last_name == "Lawrence"
            assert len(test_order_obj.products) == 2
            assert test_order_obj.products[0].product_name == \
                "Samsung Galaxy S21 Ultra"
            assert test_order_obj.products[1].product_name == "iPhone 12"
        elif test_order == "order_3":
            assert test_order_obj.customer.first_name == "Nicole"
            assert test_order_obj.customer.last_name == "Kidman"
            assert len(test_order_obj.products) == 2
            assert test_order_obj.products[0].product_name == "OnePlus 8 Pro"
            assert test_order_obj.products[1].product_name == "OnePlus 8 Pro"


@pytest.mark.happy
@mock.patch('src.main.order_management.controllers.order_controller.'
            'OrderController.get_total_price', return_value=99)
@pytest.mark.parametrize("expected", [
    [("1", "Test First Name Test Last Name", "Date Now", "Awaiting", "£99")]
])
def test_get_table_data(mock__get_total_price, order_controller, expected):
    '''Test cases for formatting data in Order instance for table.

    Order instances passed will have already gone through validation so
    this single test case is representative of all scenarios.
    '''
    order_controller._orders = {'order_1': pytest.order_one}
    table_data = order_controller.get_table_data()
    assert table_data == expected


@pytest.mark.happy
@mock.patch('src.main.order_management.controllers.order_controller.'
            'OrderController.get_product_quantities', return_value={
                                                "Test Product One": 2,
                                                "Test Product Two": 1})
@pytest.mark.parametrize("order_id, expected", [
    ("1", ("Order number 1", "Customer: Test First Name Test Last Name,\n\n"
           "Ordered items:\n  Test Product One * 2\n  Test Product Two * 1\n"
           "\nOrder date: Date Now\n\nDispatched date: Test Date\n\n"
           "Completed date: None"))
])
def test_get_order_details(mock_get_product_quantities,
                           order_controller,
                           order_id,
                           expected):
    '''Test cases for formatting Order data for output
    of details in string format for user.

    Similar to above, the passed Order instance would have
    already have been validated so this single test case
    is representative of all scenarios.
    '''
    order_controller._orders = {'order_1': pytest.order_two}
    order_details = order_controller.get_order_details(order_id)
    assert order_details == expected


@pytest.mark.happy
@mock.patch("src.main.order_management.outlook_email.update_status")
@pytest.mark.parametrize("order, expected", [
    (pytest.order_one, "Dispatched"),
    (pytest.order_two, "Complete")
])
def test_update_order_status(mock_email, order_controller, order, expected):
    '''Test cases for updating the status of an Order instance.

    Test cases include both possible scenarios:

    Awaiting -> Dispatched
    Dispatched -> Complete

    Complete order will pass through function unaffected.
    '''
    updated_order = order_controller.update_order_status(order)
    assert updated_order.status == expected
