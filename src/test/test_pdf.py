import os
import pytest
import mock
from src.main.order_management.pdf import Pdf

THIS_DIR = os.path.dirname(__file__)

@pytest.fixture
def pdf():
    return Pdf()

def test_write_picking_list(pdf):
    data = [
        ["Product ID", "Product Name", "Quantity", "Individual Price", "Aisle", "Shelf"],
        ["1", "Test Name", "2", "3.00", "4", "5"]
    ]
    picking_list_pdf = os.path.join(THIS_DIR, 'Picking List.pdf')
    pdf.write_picking_list(data, THIS_DIR)
    assert os.path.exists(picking_list_pdf) == True
    os.remove(picking_list_pdf)
    
def test_write_packaging_list(pdf):
    date = "Date"
    address = ["Deliver To:", "Test Name", "Test Line One", "Test City"]
    items = [["Item", "Quantity"], ["Item One", "2"]]
    order_id = 1
    packaging_list_pdf = os.path.join(THIS_DIR, 'Packaging List Test Name 1.pdf')
    pdf.write_packaging_list(date, address, items, order_id, THIS_DIR)
    assert os.path.exists(packaging_list_pdf) == True
    os.remove(packaging_list_pdf)

def test_write_address_label(pdf):
    address = ["Test Name", "Test Line One", "Test City"]
    order_id = 1
    address_label_pdf = os.path.join(THIS_DIR, 'Address Label Test Name 1.pdf')
    pdf.write_address_label(address, order_id, THIS_DIR)
    assert os.path.exists(address_label_pdf) == True
    os.remove(address_label_pdf)