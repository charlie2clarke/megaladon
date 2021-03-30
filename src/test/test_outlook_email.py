'''Tests the outlook_email module which contains only the update_status
function.
'''
import pytest
import mock
from src.main.order_management.outlook_email import update_status
from .models.mock_models import (
                            MockOrder,
                            MockProduct,
                            MockCustomer,
                            MockAddress,
                            setup_order)


test_order = setup_order(1, "Test First Name", "Test Last Name",
                         "testemail@something.com", "Test Line One",
                         "Test City",
                         [[1, 'Test Product One', 99.99, 1, 2],
                          [1, 'Test Product One', 99.99, 1, 2],
                          [2, 'Test Product Two', 11.11, 2, 4],
                          [3, 'Test Product Three', 22.22, 1, 1]],
                         "Awaiting", "Test Date")

test_products_and_quantities = {'Product One': 2, 'Product Two': 1}


@pytest.mark.happy
@mock.patch('src.main.order_management.outlook_email.win32com.client')
@pytest.mark.parametrize('order_instance, products_and_quantities, expected', [
    (test_order, test_products_and_quantities, ('Your order has been \
        dispatched', 'Dear Test First Name Test Last Name,\n\nYour order \
        of:\n  Product One * 2\n  Product Two * 1\n\nWas Dispatched on: \
        Date Now'))
])
def test_update_status(mock_win32_client,
                       order_instance,
                       products_and_quantities,
                       expected):
    '''Test case when email is successfully created using win32client.'''
    test_email = update_status(order_instance, products_and_quantities)
    assert test_email == expected


@pytest.mark.sad
@mock.patch('src.main.order_management.outlook_email.win32com.client.Dispatch',
            return_value=Exception)
@pytest.mark.parametrize('order_instance, products_and_quantities, expected', [
    (test_order, test_products_and_quantities, ('Your order has been \
     dispatched', 'Dear Test First Name Test Last Name,\n\nYour order of:\n  \
     Product One * 2\n  Product Two * 1\n\nWas Dispatched on: Date Now'))
])
def test_update_status(mock_win32_client,
                       order_instance,
                       products_and_quantities,
                       expected):
    '''Test case when email fails to be opened in outlook client.'''
    with pytest.raises(Exception) as exception_info:
        update_status(order_instance, products_and_quantities)
    assert "Exception" in str(exception_info.value)
