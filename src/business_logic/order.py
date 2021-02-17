from data.data_access.data_access import DataAccess
from .product import Product
from .customer import Customer
from .platform import Platform
from data.queries.query import Query

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
        self.query = Query()
        self.product = Product()
        self.customer = Customer()
        self.platform = Platform()
        self.status = status 
        self.created_date = created_date
        self.dispatched_date = dispatched_date
        self.completed_date = completed_date
        self.postage = postage

    


