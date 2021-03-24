# import pytest
# import mock
# from unittest.mock import Mock
# from datetime import datetime
# from src.test.models.mock_models import Address, Customer, Product, Order
# from src.main.order_management.models.order import Order
# from src.main.order_management.models.product import Product
# from src.main.order_management.models.customer import Customer
# from src.main.order_management.models.address import Address
# from src.main.order_management.controllers.order_controller import OrderController


# @pytest.fixture
# def order_controller():
#     return OrderController()


# @mock.patch('src.main.order_management.models.order.Order')
# def mock_order(mock_order):
#     return mock_order


# @mock.patch('src.main.order_management.models.product.Product')
# def mock_product(mock_product):
#     return mock_product


# @mock.patch('src.main.order_management.models.customer.Customer')
# def mock_customer(mock_customer):
#     return mock_customer


# @mock.patch('src.main.order_management.models.address.Address')
# def mock_address(mock_address):
#     return mock_address


# def setup_order(order_id, first_name, last_name, email, line_one, city, products, status):
#     address = Mock(Address(line_one, None, city, None))
#     customer = Mock(Customer(address, first_name, last_name, email))
#     if products is not None:
#         products = [Mock(Product(*product)) for product in products]
#     return Mock(Order(order_id, products, customer, "Awaiting", "Date Now", None, , "1st Class"))


# pytest.order_one = setup_order(1, 'Test First Name', 'Test Last Name', 'testemailone@something.com', 'Test Line One', 'Test City', 
#     [[1, 'Test Product One', 99.99, 1, 2], [1, 'Test Product One', 99.99, 1, 2], [
#         2, 'Test Product Two', 11.11, 2, 4], [3, 'Test Product Three', 22.22, 1, 1]], "Awaiting")

# pytest.order_two = setup_order(1, 'Test First Name', 'Test Last Name', 'testemailtwo@something.com', 'Test Line One', 'Test City', 
#     [[1, 'Test Product One', -5, 1, 2], [1, 'Test Product One', 2, 1, 2], [
#         2, 'Test Product Two', 2.999, 2, 4], [3, 'Test Product Three', 4.00, 1, 1]], "Awaiting")



# @pytest.mark.parametrize("order, expected", [
#     (pytest.order_one.products, 233.30999999999997),
#     (pytest.order_two.products, 3.999)
# ])
# def test__get_total_price(order_controller, order, expected):
#     total_price = order_controller._get_total_price(order)
#     assert total_price == expected


# @pytest.mark.parametrize("order, expected", [
#     (pytest.order_one, {'Test Product One': 2, 'Test Product Three': 1, 'Test Product Two': 1})
# ])
# def test_get_product_quantities(order_controller, order, expected):
#     products_and_quantities = order_controller.get_product_quantities(order)
#     assert products_and_quantities == expected


# def test_initialise_orders(order_controller):
#     initialise_orders_test_data = [
#         (1, 'Oppo Find X2 Pro', 1, 'George', 'Clooney', 'george.clooney@gmail.com', '98 Prospect Park',
#          None, 'Newcastle', None, 'Awaiting', '2021-03-16', None, None, "2nd Class", 899.0, 4, 4, 6),
#         (2, 'Samsung Galaxy S21 Ultra', 1, 'Jennifer', 'Lawrence', 'jennifer.lawrence@gmail.com',
#          '25 Landsdowne Terrace', None, 'York', None, 'Awaiting', '2021-03-16', None, None, "2nd Class", 799.0, 1, 1, 3),
#         (2, 'iPhone 12', 1, 'Jennifer', 'Lawrence', 'jennifer.lawrence@gmail.com', '25 Landsdowne Terrace',
#          None, 'York', None, 'Awaiting', '2021-03-16', None, None, "2nd Class", 1299.0, 3, 2, 5),
#         (3, 'OnePlus 8 Pro', 2, 'Nicole', 'Kidman', 'nicole.kidman@gmail.com', '15 Prospect Park',
#          None, 'Exeter', None, 'Awaiting', '2021-03-16', None, None, '2nd Class', 429.0, 2, 3, 4)
#     ]
#     initialised_orders = order_controller.initialise_orders(
#         initialise_orders_test_data)

#     for test_order in initialised_orders:
#         test_order_obj = initialised_orders[test_order]
#         if test_order == "order_1":
#             assert test_order_obj.customer.first_name == "George"
#             assert test_order_obj.customer.last_name == "Clooney"
#             assert len(test_order_obj.products) == 1
#             assert test_order_obj.products[0].product_name == "Oppo Find X2 Pro"
#         elif test_order == "order_2":
#             assert test_order_obj.customer.first_name == "Jennifer"
#             assert test_order_obj.customer.last_name == "Lawrence"
#             assert len(test_order_obj.products) == 2
#             assert test_order_obj.products[0].product_name == "Samsung Galaxy S21 Ultra"
#             assert test_order_obj.products[1].product_name == "iPhone 12"
#         elif test_order == "order_3":
#             assert test_order_obj.customer.first_name == "Nicole"
#             assert test_order_obj.customer.last_name == "Kidman"
#             assert len(test_order_obj.products) == 2
#             assert test_order_obj.products[0].product_name == "OnePlus 8 Pro"
#             assert test_order_obj.products[1].product_name == "OnePlus 8 Pro"
        

# @mock.patch('src.main.order_management.controllers.order_controller.OrderController._get_total_price', return_value=99)
# @pytest.mark.parametrize("expected", [
#     [("1", "Test First Name Test Last Name", "Test Date", "Awaiting", "£99")]
# ])
# def test_get_table_data(mock__get_total_price, order_controller, expected):
#     order_controller._orders = {'order_1': pytest.order_one}
#     table_data = order_controller.get_table_data()
#     assert table_data == expected


# @mock.patch('src.main.order_management.controllers.order_controller.OrderController.get_product_quantities', return_value={"Test Product One": 2, "Test Product Two": 1})
# @pytest.mark.parametrize("order_id, expected", [
#     ("1", ("Order number 1", "Customer: Test First Name Test Last Name,\n\nOrdered items:\n  Test Product One * 2\n  "
#            "Test Product Two * 1\n\nOrder date: Test Date\n\nDispatched date: Date Now\n\nCompleted date: None"))
# ])
# def test_get_order_details(mock_get_product_quantities, order_controller, order_id, expected):
#     order_controller._orders = {'order_1': pytest.order_one}
#     order_details = order_controller.get_order_details(order_id)
#     assert order_details == expected


# @mock.patch("src.main.order_management.outlook_email.update_status")
# @pytest.mark.parametrize("order, expected", [
#     (['1', None, None, 'Awaiting'], [{'order_1': pytest.order_one}])
# ])
# def test_update_order_status(mock_email, order_controller, order, expected):
#     order_controller._orders = {'order_1': pytest.order_one}
#     updated_order = order_controller.update_order_status(order)
#     assert updated_order.status == expected[0]['order_1'].status
