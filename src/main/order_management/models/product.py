'''Represents data stored on a single product ordered by customer.

Each product should have own instance of this class.

Includes details of location in warehouse.
'''


class Product:
    '''Class representing data stored on a single product ordered.'''

    def __init__(self, product_id, product_name, price, aisle, shelf):
        '''Inits Product.

        Args:
            product_id: an integer of the ID of a product, acting as
                        a unique identifer for the product.
            product_name: a string of the name of the product.
            price: floating point of the individual price of the product.
            aisle: an integer of the aisle in warehouse product is located.
            shelf: an integer of the shelf in warehouse product is located.
        '''
        self._product_id = product_id
        self._product_name = product_name
        self._price = price
        self._aisle = aisle
        self._shelf = shelf

    @property
    def product_id(self):
        '''Integer that uniquely identifies the product.'''
        return self._product_id

    @property
    def product_name(self):
        '''String of the product name.'''
        return self._product_name

    @property
    def price(self):
        '''Floating point of the individual price of the product.'''
        return self._price

    @property
    def aisle(self):
        '''Integer of the aisle in warehouse product is located.'''
        return self._aisle

    @property
    def shelf(self):
        '''Integer of shelf in warehouse product is located.'''
        return self._shelf
