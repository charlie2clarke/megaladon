from kivymd.uix.datatables import MDDataTable


class DataTable:
    def create_data_table(self, column_data, row_data, on_row_press, on_check_press):
        table = MDDataTable(
            size_hint=(1, 0.85),
            check=True,
            column_data=column_data,
            row_data=row_data,
            rows_num=len(row_data)
        )
        table.bind(on_row_press=on_row_press)
        table.bind(on_check_press=on_check_press)
       
        return table
