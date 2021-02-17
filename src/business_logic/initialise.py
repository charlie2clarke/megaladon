from data.query import Query

class Initialise:
    def __init__(self):
        self.query = Query()
        self.all_data = self.query.get_all_data()
        self.initialise_classes()

    def initialise_classes(self):
        return True
        # for i in range(len(self.all_data)):
        #     self.product + "i" = Product(items_and_quantity=)
        #     self.order + "i" = Order(product=self.all_data[i][], customer=self.all_data[i][], status=self.all_data[i][9],\
        #         created_date=self.all_data[i][10], dispatched_date=self.all_data[i][11], completed_date=self.all_data[i][12],\
        #             postage=self.all_data[i][13]) 
    
