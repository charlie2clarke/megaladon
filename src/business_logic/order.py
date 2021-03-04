from data.data_access import DataAccess
from .product import Product
from .customer import Customer
from .platform import Platform
from data.query import Query

class Order:
    def __init__(
            self, 
            product, 
            customer, 
            status, 
            created_date, 
            dispatched_date,
            completed_date, 
            postage
        ):
        self._query = Query()
        self.product = product
        self.customer = customer
        self._status = status
        self._created_date = created_date
        self._dispatched_date = dispatched_date
        self._completed_date = completed_date
        self._postage = postage

    @property
    def created_date(self):
        return self._created_date

    @property
    def dispatched_date(self):
        return self._dispatched_date

    @dispatched_date.setter
    def dispatched_date(self, value):
        self._dispatched_date = value

    @property
    def completed_date(self):
        return self._completed_date

    @completed_date.setter
    def completed_date(self, value):
        self._completed_date = value

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, new_status):
        self._status = new_status
