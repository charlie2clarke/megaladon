import pytest
from unittest.mock import patch
from main.business_logic.address_label import AddressLabel


class Address:
    def __init__(self, line_one, line_two, city):
        self.line_one = line_one
        self.line_two = line_two
        self.city = city


class Customer:
    def __init__(self, address, first_name, last_name):
        self.address = address
        self.first_name = first_name
        self.last_name = last_name


class Order:
    def __init__(self, customer):
        self.customer = customer


class OrderController:
    orders = {
        'order_1': Order(customer=setup_customer())
    }

    def __init__(self, x):
        print("HFUEIHUIFHEUIHH*************")
        pass
    
    @staticmethod
    def setup_customer():
        def setup_address():
            return Address(line_one='Test Line One',
                                line_two='Test Line Two', city='Test City')

        address = setup_address()
        return Customer(address=address, first_name='Test First Name', last_name='Test Last Name')


@patch("main.business_logic.address_label.OrderContoller", new_callable=OrderController)
def test_address_label(mock_controller):
    address_label = AddressLabel()
    orders_selected = [['1', 'Test Name', '2021-03-12', 'Status', '£200']]
    scenario_one_address = ['Test First Name Test Last Name', 'Test Line One', 'Test City'] 

    address_label_contents = address_label.create_address_label(
        orders_selected)
    assert address_label_contents == (scenario_one_address, 1, 0)
