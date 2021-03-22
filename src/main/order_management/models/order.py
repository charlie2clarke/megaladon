'''Represents data stored on an order.

Is the main reference for data, and is made up of
other objects.
'''


class Order:
    '''A class representing data stored on an order.'''

    def __init__(
            self,
            order_id,
            products,
            customer,
            status,
            created_date,
            dispatched_date,
            completed_date,
            postage
            ):
        '''Inits Order.

        Args:
            order_id: The integer ID of the order.
            products: an array of Product instances for the order. Each
                      product should have own instance and quantities
                      can be calculated using get_products_and_quantities
                      method in OrderController.
            customer: an instance of Customer who completed the order.
            status: a string of status of order, can either be: 'Awaiting',
                    'Dispatched' or 'Completed'.
            created_date: a string of the date the order was created.
            dispatched_date: a string of the date the order was dispatched
                             (could be None).
            completed_date: a string of the date the order was completed
                            (could be None).
            postage: a string of type of postage requested.
        '''
        self._order_id = order_id
        self._products = products
        self._customer = customer
        self._status = status
        self._created_date = created_date
        self._dispatched_date = dispatched_date
        self._completed_date = completed_date
        self._postage = postage

    @property
    def products(self):
        '''An array of Product instances.'''
        return self._products

    @property
    def customer(self):
        '''An instance of Customer.'''
        return self._customer

    @property
    def order_id(self):
        '''An integer of order ID to act as a unique identifier for order.'''
        return self._order_id

    @property
    def created_date(self):
        '''A string of date order was created.

        Isn't prescriptive of format entered, but format currently using is:
        yyyy-mm-dd.
        '''
        return self._created_date

    @property
    def dispatched_date(self):
        '''A string of date order was dispatched - could be None if
        not yet dispatched.

        Isn't prescriptive of format entered, but format currently using is:
        yyyy-mm-dd.
        '''
        return self._dispatched_date

    @dispatched_date.setter
    def dispatched_date(self, value):
        '''Sets new string dispatched date value.

        Format: yyyy-mm-dd.
        '''
        self._dispatched_date = value

    @property
    def completed_date(self):
        '''A string of date order was completed - could be None if
        not yet completed.

        Isn't prescriptive of format entered, but format currently using is:
        yyyy-mm-dd.
        '''
        return self._completed_date

    @completed_date.setter
    def completed_date(self, value):
        '''Sets new string completed date value.

        Format: yyyy-mm-dd.
        '''
        self._completed_date = value

    @property
    def status(self):
        '''A string of the status of an order.

        Can be either: 'Awaiting', 'Dispatched' or 'Completed'.
        '''
        return self._status

    @status.setter
    def status(self, new_status):
        '''Sets new string status of order.

        Either: 'Awaiting', 'Dispatched' or 'Completed'.
        '''
        self._status = new_status
