import pytest
import mock
from src.main.order_management.outlook_email import update_status
from .models.mock_models import Order, Product, Customer, Address


def set_up():
    address = Address(line_one="Test Line One", city="Test City")
    customer = Customer(
        address=address, first_name="Test First Name", last_name="Test Last Name", email="testemail@something.com")
    order_instance = Order(order_id=1, customer=customer, products=None,
                           created_date="Test Created Date", status="Dispatched")
    products_and_quantities = {'Product One': 2, 'Product Two': 1}
    return order_instance, products_and_quantities

@pytest.mark.happy
@mock.patch('src.main.order_management.outlook_email.win32com.client')
@pytest.mark.parametrize('order_instance, products_and_quantities, expected', [
    (set_up()[0], set_up()[1], ('Your order has been dispatched', 'Dear Test First Name Test Last Name,\n\nYour order of:\n  Product One * 2\n  Product Two * 1\n\nWas Dispatched on: Date Now'))
])
def test_update_status(mock_win32_client, order_instance, products_and_quantities, expected):
    test_email = update_status(order_instance, products_and_quantities)
    assert test_email == expected

# @pytest.mark.sad
# @mock.patch('src.main.order_management.outlook_email.win32com.client.Dispatch', side_effect=Exception(Exception))
# @pytest.mark.parametrize('order_instance, products_and_quantities, expected', [
#     (set_up()[0], set_up()[1], ('Your order has been dispatched', 'Dear Test First Name Test Last Name,\n\nYour order of:\n  Product One * 2\n  Product Two * 1\n\nWas Dispatched on: Date Now'))
# ])
# def test_update_status(mock_win32_client, order_instance, products_and_quantities, expected):
#     with pytest.raises(Exception) as exception_info:
#         update_status(order_instance, products_and_quantities)
#     assert "Error occured" in str(exception_info.value)