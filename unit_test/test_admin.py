import unittest
from unittest.mock import patch, MagicMock
from users.admin import Admin

class TestAdmin(unittest.TestCase):

    @patch('users.admin.Database')
    @patch('users.admin.RequestHandler')
    def setUp(self, MockRequestHandler, MockDatabase):
        self.mock_db = MockDatabase.return_value
        self.mock_request_handler = MockRequestHandler.return_value
        self.admin = Admin(user={'name': 'AdminUser'})
        
    @patch('builtins.input', side_effect=['Pizza', '12', 'True', 'Main Course'])
    def test_add_item(self, mock_input):
        expected_request = {
            'client_type': 'admin',
            'action': 'add_item',
            'item_name': 'Pizza',
            'item_price': '12',
            'availability': 'True',
            'category': 'Main Course'
        }

        request_data = self.admin.add_item()
        self.assertEqual(request_data, expected_request)
        
    @patch('builtins.input', side_effect=[1, 1, 'Pasta'])
    def test_update_item(self, mock_input):
        expected_request = {
            'client_type': 'admin',
            'action': 'update_item',
            'item_id': 1,
            'updating_field': 'Item Name',
            'updating_value': 'Pasta'
        }

        request_data = self.admin.update_item()
        self.assertEqual(request_data, expected_request)
        
    @patch('builtins.input', side_effect=[1])
    def test_remove_item(self, mock_input):
        expected_request = {
            'client_type': 'admin',
            'action': 'remove_item',
            'item_id': 1
        }

        request_data = self.admin.remove_item()
        self.assertEqual(request_data, expected_request)
        

if __name__ == '__main__':
    unittest.main()
