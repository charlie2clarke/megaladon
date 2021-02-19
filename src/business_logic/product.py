class Product:
    instances = []

    def __init__(self, items_and_quantity):
        self.items_and_quantity = items_and_quantity
        self.__class__.instances.append(self)
    
    @classmethod
    def list_all_objects(cls):
        for instance in cls.instances:
            print(instance)

