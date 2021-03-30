'''Sets configuration for testing of app.'''
import os

TEST_DIR = os.path.dirname(__file__)
TEST_DATABASE = os.path.join(TEST_DIR, 'data', 'database',
                             'TestOnlineStore.db')
