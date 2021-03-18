from .controllers.test_order_controller import Order as TestOrder
from src.main.order_management.models.order import Order as MainOrder

def pytest_assertrepr_compare(op, left, right):
    if isinstance(left, MainOrder) and isinstance(right, TestOrder) and op == "==":
        return left.customer.first_name == right.customer.first_name