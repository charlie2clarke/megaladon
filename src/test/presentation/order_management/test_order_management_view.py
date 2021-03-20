import pytest
import mock
from src.main.order_management.presentation.order_management.order_management_view import OrderManagementScreen

@pytest.fixture
def order_management_screen():
    return OrderManagementScreen()

# def test_on_row_press():
    