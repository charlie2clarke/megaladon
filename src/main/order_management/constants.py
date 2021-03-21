'''Stores constant variables.'''
import os
from pathlib import Path

SENDER_DETAILS = ['Sender:', 'Awesome Organisation Inc.',
                  'Building Abbey Road', 'London', 'L2C 802', '12345 678910']

HELP_TEXT = "All orders can be seen in the table with awaiting ones at "\
    "the top. Click on the row to see more info on the specific order, " \
    "or click on the checkbox to select one/mutiple orders and then execute" \
    " one of the listed actions on the selected order(s) by clicking the " \
    "buttons."

BASE_DIR = os.path.dirname(__file__)
PICKING_LIST_DIR = os.path.abspath(
    os.path.join(BASE_DIR, '../../..', 'picking_list'))
PACKAGING_LIST_DIR = os.path.abspath(
    os.path.join(BASE_DIR, '../../..', 'packaging_lists'))
ADDRESS_LABELS_DIR = os.path.abspath(
    os.path.join(BASE_DIR, '../../..', 'address_labels'))
DATABASE = os.path.join(BASE_DIR, 'data/database', 'OnlineStore.db')

WEBAY_URL = 'http://localhost:8080'
