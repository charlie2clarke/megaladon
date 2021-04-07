'''Test for RequestController

Uses responses library https://github.com/getsentry/responses
to help mock responses from Webay API.

Tests have custom markers (defined in pytest.ini) to define happy
and sad paths that are possible when invoking this class.

Custom markers allow specific test to be run for example using:
$ pytest -m sad
'''
import pytest
import mock
import responses
from requests.exceptions import HTTPError, Timeout, ConnectionError
from src.main.order_management.controllers.request_controller \
    import RequestController


# Fixture allows for a cleaner way to instantiate class that is being tested.
@pytest.fixture
def request_controller():
    return RequestController()


@pytest.mark.happy
@responses.activate
def test_get_new_orders(request_controller):
    '''Test case for a successful response from Webay API (response code 200).
    That doesn't have any new orders responded with.
    '''
    responses.add(responses.GET, 'http://localhost:8080', json=[], status=200)
    new_orders = request_controller.get_new_orders()
    assert len(new_orders) == 0


@pytest.mark.happy
@responses.activate
def test_get_new_orders(request_controller):
    '''Test case for a single customer with one item.

    Ref 2 in report.
    '''
    responses.add(responses.GET, 'http://localhost:8080',
                  json=[{'address': 'Test Address One, Test City One',
                         'item': 'Test Item One', 'name': 'Test Customer One',
                         'price': 888}],
                  status=200)

    new_orders = request_controller.get_new_orders()
    expected = [
        [
            [
                {'item': 'Test Item One',
                    'quantity': 1}
            ],
            'Test',
            'Customer One',
            'Test Address One',
            None,
            'Test City One',
            'test.customerone@gmail.com',
            2
        ]
    ]
    assert new_orders == expected


@pytest.mark.happy
@responses.activate
def test_get_new_orders(request_controller):
    '''Test case for multiple customers with a single item.

    Ref 3 in report.
    '''
    responses.add(responses.GET, 'http://localhost:8080',
                  json=[{'address': 'Test Address One, Test City One',
                         'item': 'Test Item One', 'name': 'Test Customer One',
                         'price': 888},

                        {'address': 'Test Address Two, Test Line Two, \
                         Test City Two', 'item': 'Test Item Two',
                         'name': 'Test Customer Two', 'price': 44}],
                  status=200)

    new_orders = request_controller.get_new_orders()
    expected = [
        [
            [
                {'item': 'Test Item One',
                    'quantity': 1}
            ],
            'Test',
            'Customer One',
            'Test Address One',
            None,
            'Test City One',
            'test.customerone@gmail.com',
            2
        ],
        [
            [
                {'item': 'Test Item Two',
                    'quantity': 1}
            ],
            'Test',
            'Customer Two',
            'Test Address Two',
            'Test Line Two',
            'Test City Two',
            'test.customertwo@gmail.com',
            3
        ]
    ]
    assert new_orders == expected


@pytest.mark.happy
@responses.activate
def test_get_new_orders(request_controller):
    '''Test case for a single customer with multiple of one item.

    Ref 4 in report.
    '''
    responses.add(responses.GET, 'http://localhost:8080',
                  json=[{'address': 'Test Address Three, Test City Three',
                         'item': 'Test Item Three', 'name': 'Test Customer \
                          Three', 'price': 1440},

                        {'address': 'Test Address Three, Test City Three',
                         'item': 'Test Item Three', 'name': 'Test Customer \
                          Three', 'price': 1440}],
                  status=200)

    new_orders = request_controller.get_new_orders()
    expected = [
        [
            [
                {'item': 'Test Item Three',
                    'quantity': 2}
            ],
            'Test',
            'Customer Three',
            'Test Address Three',
            None,
            'Test City Three',
            'test.customerthree@gmail.com',
            1
        ]
    ]
    assert new_orders == expected


@pytest.mark.happy
@responses.activate
def test_get_new_orders(request_controller):
    '''Test case for a single customer with multiple of varying item.

    Ref 5 in report.
    '''
    responses.add(responses.GET, 'http://localhost:8080',
                  json=[{'address': 'Test Address One, Test City One',
                         'item': 'Test Item One', 'name': 'Test Customer One',
                         'price': 888},
                        {'address': 'Test Address One, Test City One',
                         'item': 'Test Item Two', 'name': 'Test Customer One',
                         'price': 44}],
                  status=200)

    new_orders = request_controller.get_new_orders()
    expected = [
        [
            [
                {'item': 'Test Item One',
                    'quantity': 1},
                {'item': 'Test Item Two',
                    'quantity': 1}
            ],
            'Test',
            'Customer One',
            'Test Address One',
            None,
            'Test City One',
            'test.customerone@gmail.com',
            2
        ]
    ]
    assert new_orders == expected


@pytest.mark.happy
@responses.activate
def test_get_new_orders(request_controller):
    '''Responses.add is essentially defining test data, and have included every
    possible edge case from a successful response with at least one order
    from Webay API.

    That is:
        Customer ordering one product.
        Customer order multiple different products - retrieved as separate
           entries (and not sequentially).
        Customer ordering multiple of the same product.

    Ref 6 in report.
    '''
    responses.add(responses.GET, 'http://localhost:8080',
                  json=[{'address': 'Test Address One, Test City One',
                         'item': 'Test Item One', 'name': 'Test Customer One',
                         'price': 888},

                        {'address': 'Test Address Two, Test Line Two, \
                         Test City Two', 'item': 'Test Item Two',
                         'name': 'Test Customer Two', 'price': 44},

                        {'address': 'Test Address One, Test City One',
                         'item': 'Test Item Two', 'name': 'Test Customer One',
                         'price': 44},

                        {'address': 'Test Address Three, Test City Three',
                         'item': 'Test Item Three', 'name': 'Test Customer \
                          Three', 'price': 1440},

                        {'address': 'Test Address Three, Test City Three',
                         'item': 'Test Item Three', 'name': 'Test Customer \
                          Three', 'price': 1440}],
                  status=200)
    new_orders = request_controller.get_new_orders()
    expected = [
        [
            [
                {'item': 'Test Item One',
                    'quantity': 1},
                {'item': 'Test Item Two',
                    'quantity': 1}
            ],
            'Test',
            'Customer One',
            'Test Address One',
            None,
            'Test City One',
            'test.customerone@gmail.com',
            2
        ],
        [
            [
                {'item': 'Test Item Three',
                 'quantity': 2}
            ],
            'Test',
            'Customer Three',
            'Test Address Three',
            None,
            'Test City Three',
            'test.customerthree@gmail.com',
            4
        ],
        [
            [
                {'item': 'Test Item Two',
                 'quantity': 1}
            ],
            'Test',
            'Customer Two',
            'Test Address Two',
            'Test Line Two',
            'Test City Two',
            'test.customertwo@gmail.com',
            5
        ],
    ]
    assert new_orders == expected


@pytest.mark.sad
@responses.activate
def test_get_new_orders(request_controller):
    '''Test case for when HTTPError is raised.

    Ref 7 in report.
    '''
    responses.add(responses.GET, 'http://localhost:8080/',
                  body=Exception(HTTPError))
    with pytest.raises(Exception) as exception_info:
        request_controller.get_new_orders()
    assert "HTTPError" in str(exception_info.value)


@pytest.mark.sad
@responses.activate
def test_get_new_orders(request_controller):
    '''Test case for when Timeout is raised.

    Ref 8 in report.
    '''
    responses.add(responses.GET, 'http://localhost:8080/',
                  body=Exception(Timeout))
    with pytest.raises(Exception) as exception_info:
        request_controller.get_new_orders()
    assert "Timeout" in str(exception_info.value)


@pytest.mark.sad
@responses.activate
def test_get_new_orders(request_controller):
    '''Test for when ConnectionError is raised.

    Ref 9 in report.
    '''
    responses.add(responses.GET, 'http://localhost:8080/',
                  body=Exception(ConnectionError))
    with pytest.raises(Exception) as exception_info:
        request_controller.get_new_orders()
    assert "ConnectionError" in str(exception_info.value)
