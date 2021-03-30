'''Tests the Pdf class.

The contents of pdf files created from this class should be tested
manually, however, the tests in this file test that they are successfully
created with a given set of data, with the expected file name and in the
expected location.
'''
import os
import pytest
import mock
from src.main.order_management.pdf import Pdf
from src.test.test_config import TEST_DIR


@pytest.fixture
def pdf():
    return Pdf()


@pytest.mark.happy
def test_write_picking_list(pdf):
    '''Tests picking list is created successfully.'''
    data = [
        ["Product ID", "Product Name", "Quantity", "Individual Price",
         "Aisle", "Shelf"],
        ["1", "Test Name", "2", "3.00", "4", "5"]
    ]
    picking_list_pdf = os.path.join(TEST_DIR, 'Picking List.pdf')
    pdf.write_picking_list(data, TEST_DIR)
    does_exist = os.path.exists(picking_list_pdf)
    assert does_exist is True
    if does_exist is True:
        os.remove(picking_list_pdf)


@pytest.mark.happy
def test_write_packaging_list(pdf):
    '''Test packaging list is created successfully.'''
    date = "Date"
    address = ["Deliver To:", "Test Name", "Test Line One", "Test City"]
    items = [["Item", "Quantity"], ["Item One", "2"]]
    order_id = 1
    packaging_list_pdf = os.path.join(TEST_DIR,
                                      'Packaging List Test Name 1.pdf')
    pdf.write_packaging_list(date, address, items, order_id, TEST_DIR)
    does_exist = os.path.exists(packaging_list_pdf)
    assert does_exist is True
    if does_exist is True:
        os.remove(packaging_list_pdf)


@pytest.mark.happy
def test_write_address_label(pdf):
    '''Tests address label is created successfully.'''
    address = ["Test Name", "Test Line One", "Test City"]
    order_id = 1
    address_label_pdf = os.path.join(TEST_DIR, 'Address Label Test Name 1.pdf')
    pdf.write_address_label(address, order_id, TEST_DIR)
    does_exist = os.path.exists(address_label_pdf)
    assert does_exist is True
    if does_exist is True:
        os.remove(address_label_pdf)
