class Product:
    def __init__(self, product_id, product_name, price, aisle, shelf):
        self._product_id = product_id
        self._product_name = product_name
        self._price = price
        self._aisle = aisle
        self._shelf = shelf

    @property
    def product_id(self):
        return self._product_id

    @property
    def product_name(self):
        return self._product_name

    @property
    def price(self):
        return self._price

    @property
    def aisle(self):
        return self._aisle

    @property
    def shelf(self):
        return self._shelf

    # @property
    # def ordered_items(self):
    #     return self._ordered_items

    # def get_total(self, ordered_items):
    #     total = 0

    #     for dictionary in ordered_items:
    #         total = total + (dictionary['quantity']
    #                          * dictionary['individual_price'])

    #     return total
