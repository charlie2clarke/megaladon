import os
import pytest
import mock
from src.main.order_management.data.data_access import DataAccess

# THIS_DIR = os.path.dirname(__file__)
# TEST_DATABASE = os.path.join(os.path.dirname(__file__), 'database', 'TestOnlineStore.db')


@pytest.fixture
def data_access():
    return DataAccess()


# @mock.patch('src.main.order_management.data.data_access.DATABASE', return_value=os.path.join(os.path.dirname(__file__), 'database', 'TestOnlineStore.db'))
# def test__create_connection(mock_database, data_access):
#     print("*****************")
#     print(mock_database)
#     connection = data_access._create_connection()
#     assert connection is not None
