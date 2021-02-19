class Product:
    def __init__(self, items_quantity_price):
        self._items_quantity_price = items_quantity_price

    @property
    def items_quantity_price(self):
        return self._items_quantity_price

    def get_total(self, items_quantity_price):
        total = 0

        for dictionary in items_quantity_price:
            total = total + (dictionary['quantity'] * dictionary['individual_price'])

        return total

    
    # @items_quantity_price.setter
    # def items_quantity_price(self, new_items_quantity_price):
    #     self.items_quantity_price = new_items_quantity_price
    

