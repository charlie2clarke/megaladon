class Product:
    def __init__(self, ordered_items):
        self._ordered_items = ordered_items

    @property
    def ordered_items(self):
        return self._ordered_items


    def get_total(self, ordered_items):
        total = 0

        for dictionary in ordered_items:
            total = total + (dictionary['quantity'] * dictionary['individual_price'])

        return total

    
    # @ordered_items.setter
    # def ordered_items(self, new_ordered_items):
    #     self.ordered_items = new_ordered_items
    

