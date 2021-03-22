'''Sets configuration for app.

Includes required files paths and URL to contact Webay API.
'''
import os
from pathlib import Path

BASE_DIR = os.path.dirname(__file__)
PICKING_LIST_DIR = os.path.abspath(
    os.path.join(BASE_DIR, '../../..', 'picking_list'))
PACKAGING_LIST_DIR = os.path.abspath(
    os.path.join(BASE_DIR, '../../..', 'packaging_lists'))
ADDRESS_LABELS_DIR = os.path.abspath(
    os.path.join(BASE_DIR, '../../..', 'address_labels'))
DATABASE = os.path.join(BASE_DIR, 'data/database', 'OnlineStore.db')

WEBAY_URL = 'http://localhost:8080'
