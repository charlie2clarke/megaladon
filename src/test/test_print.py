import pytest
import mock
from src.main.order_management.print import Print


@mock.patch('src.main.order_management.print.win32print.EnumPrinters', return_value=[[None, None, 'printer 1'], [None, None, 'printer 2']])
@mock.patch('src.main.order_management.print.win32print.SetDefaultPrinter')
@mock.patch('src.main.order_management.print.Path.rglob', return_value=['fileaddressone.pdf'])
@mock.patch('src.main.order_management.print.win32api.ShellExecute')
@pytest.mark.parametrize('selected_printer, destination', [
    ('printer 1', 'test_destination')
])
def test_print_pdf(mock_printers, mock_default_printer, mock_paths, mock_shell_execute, selected_printer, destination):
    Print.print_pdf(selected_printer, destination)
    assert mock_shell_execute.call_count == 1