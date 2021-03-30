'''Tests Document.

Document methods all require instances of Order to format data of.
Therefore, instances of Order have been created/mocked with MockOrder.
'''
import pytest
import mock
from .models.mock_models import (
                        MockAddress,
                        MockCustomer,
                        MockProduct,
                        MockOrder,
                        setup_order
                        )
from src.main.order_management.document import Document


@pytest.fixture
def document():
    return Document()


test_order = setup_order(1, "Test First Name", "Test Last Name",
                         "testemail@something.com", "Test Line One",
                         "Test City",
                         [[1, 'Test Product One', 99.99, 1, 2],
                          [1, 'Test Product One', 99.99, 1, 2],
                          [2, 'Test Product Two', 11.11, 2, 4],
                          [3, 'Test Product Three', 22.22, 1, 1]],
                         "Awaiting", "Test Date")


picking_list_expected = [["Product ID", "Product Name", "Quantity",
                          "Individual Price", "Aisle", "Shelf"],
                         [3, "Test Product Three", 1, 22.22, 1, 1],
                         [1, "Test Product One", 2, 99.99, 1, 2],
                         [2, 'Test Product Two', 1, 11.11, 2, 4]]


# Have formatted test data like below to improve readability because there's
# quite a bit of scaffolding required to generate test data for these
# functions.
picking_list_data = [
    ([test_order], picking_list_expected)
]


@pytest.mark.happy
@mock.patch('src.main.order_management.document.Pdf.write_picking_list')
@pytest.mark.parametrize("picking_list_orders, expected", picking_list_data)
def test_create_picking_list(mock_pdf,
                             document,
                             picking_list_orders,
                             expected):
    '''Test case that all awaiting items are grouped and formatted in the
    correct order according to aisle and shelf number regardless of order
    input.
    '''
    picking_list_contents = document.create_picking_list(picking_list_orders)
    assert picking_list_contents == expected


packaging_list_products_and_quantities = {
    'Test Product 1': 2, 'Test Product 2': 4}
packaging_list_test_data = [
    (test_order, packaging_list_products_and_quantities, ([
     "Deliver To:", "Test First Name Test Last Name", "Test Line One",
     "Test City"],
     [['Item', 'Quantity'], ['Test Product 1', 2],
      ['Test Product 2', 4]]))
]


@pytest.mark.happy
@mock.patch('src.main.order_management.document.Pdf.write_packaging_list')
@pytest.mark.parametrize("packaging_list_order, \
                         packaging_list_products_and_quantities, \
                         expected", packaging_list_test_data)
def test_create_packaging_label(mock_pdf,
                                document,
                                packaging_list_order,
                                packaging_list_products_and_quantities,
                                expected):
    '''Test case for seeing that the contents of a packaging list are
    correctly formatted for a given order - one with multiple products
    and quantities.
    '''
    packaging_list_contents = document.create_packaging_list(
        packaging_list_order, packaging_list_products_and_quantities)
    assert packaging_list_contents == expected


address_label_test_data = [
    (test_order, [
     "Test First Name Test Last Name", "Test Line One", "Test City"]),
]


@pytest.mark.happy
@mock.patch('src.main.order_management.document.Pdf.write_address_label')
@pytest.mark.parametrize("address_label_order, expected",
                         address_label_test_data)
def test_create_address_label(mock_pdf,
                              document,
                              address_label_order,
                              expected):
    '''Test case that address label is created correctly.

    Edge cases don't need to be tested because order and address will be
    validated externally from this class.
    '''
    address_label_contents = document.create_address_label(
        address_label_order)
    assert address_label_contents == expected
