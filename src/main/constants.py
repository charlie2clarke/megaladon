import os

SENDER_DETAILS = ['Sender:', 'Awesome Organisation Inc.',
                  'Building Abbey Road', 'London', 'L2C 802', '12345 678910']

BASE_DIR = os.path.dirname(__file__)
PICKING_LIST_DIR = os.path.abspath(os.path.join(BASE_DIR, '../..', 'picking_list'))
PACKAGING_LIST_DIR = os.path.abspath(os.path.join(BASE_DIR, '../..', 'packaging_lists'))
ADDRESS_LABELS_DIR = os.path.abspath(os.path.join(BASE_DIR, '../..', 'address_labels'))

URL = 'http://localhost:8080'
