from kivymd.uix.datatables import MDDataTable

class DataTable(MDDataTable):
    def __init__(self, column_data, row_data):
        self.column_data = column_data
        self.row_data = row_data

    def create_data_table(self):
        return MDDataTable(
            size_hint=(1, 0.85),
            # use_pagination=True,
            check=True,
            column_data=self.column_data,
            row_data=self.row_data
        )
