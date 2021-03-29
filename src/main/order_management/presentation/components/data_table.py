'''Reusable KivyMDDataTable component.

KivyMDDataTable is a table with x number of headings and rows
gives on row press and on row check functionality.
'''
from kivymd.uix.datatables import MDDataTable


class DataTable:
    '''MDDataTable component.

    Have separated to increase cohesion, with the thought that data tables
    on new pages are likely to be used.

    Have implemented as a class because Kivy requires reference to instance
    variables.
    '''
    def __init__(self, column_data):
        self.column_data = column_data
        self.row_data = []
        self.rows_checked = []

    def create_data_table(self,
                          row_data,
                          on_row_press,
                          on_check_press
                          ):
        '''Creates data table with passed row and column data.

        Uses a default configuration of no pagination - displaying
        all rows on one page due to buggy behaviour.

        Args:
            column_data: an array of column headings with a tuple for each
                         column with first item as string of column name
                         and second item as column width.
            row_data: an array of row data, each row is a tuple with
                      every item a string in corresponding order to column
                      names.
            on_row_press: callback function to bind when entire row is pressed.
            on_check_press: callback function to bind when checkbox is pressed+col

        Returns:
            Instance of MDDataTable - must be assigned to instance variable.
        '''
        if row_data is not None:
            self.row_data = row_data

        table = MDDataTable(
            size_hint=(1, 0.85),
            check=True,
            column_data=self.column_data,
            row_data=self.row_data,
            rows_num=len(self.row_data)
        )
        table.bind(on_row_press=on_row_press)
        table.bind(on_check_press=on_check_press)

        return table
