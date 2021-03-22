import os
import pytest
import mock
from src.main.order_management.data.data_access import DataAccess

THIS_DIR = os.path.dirname(__file__)
TEST_DATABASE = os.path.join(THIS_DIR, 'database', 'TestOnlineStore.db')


@pytest.fixture
def data_access():
    return DataAccess()


@mock.patch('src.main.order_management.config.DATABASE',
            return_value=TEST_DATABASE)
def test__create_connection(mock_database, data_access):
    connection = data_access._create_connection()
    assert connection is not None

# @mock.patch('src.main.order_management.constants.DATABASE',
#              return_value=TEST_DATABASE)
# @mock.patch('src.main.order_management.data.data_access.sqlite3.dbapi2')
# def test_execute(mock_database, mock_cursor, data_access):
#     mock_execute = mock_cursor.connect().cursor().execute
#     data_access.execute("SELECT * FROM Address", None)
#     mock_execute.assert_called_with("query")
