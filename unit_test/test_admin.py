import unittest
from unittest.mock import patch, Mock
from admin.admin_controller import AdminController
from admin.admin_service import AdminService
from admin.admin_repository import AdminRepository

class TestAdminFunctionalities(unittest.TestCase):
    
    @patch('admin.admin_repository.Database')
    def setUp(self, MockDatabase):
        self.mock_db = MockDatabase.return_value
        self.admin_repository = AdminRepository()
        self.admin_service = AdminService(self.admin_repository)
        self.admin_controller = AdminController()

    def test_add_food_item_success(self):
        food_item_data = {
            'name': 'Sphegati',
            'price': '150',
            'availability': 'Lunch',
            'category': 'Vegetarian',
            'food_type': 'Fast Food',
            'spice_level': 'Medium',
            'preference': 'Italian'
        }
        response = {'status': 'success', 'message': 'Item added successfully', 'item_id': 1}
        self.admin_repository.add = Mock(return_value=response)
        
        result = self.admin_service.add_food_item(food_item_data)
        
        self.assertEqual(result, response)
    
    def test_update_food_item_success(self):
        food_item_data = {
            'id': 1,
            'updating_field': 'Price',
            'updating_value': '200'
        }
        response = {'status': 'success', 'message': 'Pasta\'s price is updated to 200.', 'item_id': 1}
        self.admin_repository.update = Mock(return_value=response)
        
        result = self.admin_service.update_food_item(food_item_data)
        
        self.assertEqual(result, response)

    def test_remove_food_item_success(self):
        food_item_data = {'id': 1}
        response = {'status': 'success', 'message': 'Pasta is removed from cafeteria.', 'item_id': 1}
        self.admin_repository.remove = Mock(return_value=response)
        
        result = self.admin_service.remove_food_item(food_item_data)

        self.assertEqual(result, response)
    
    def test_view_menu_success(self):
        menu = [
            (1, 'Pasta', '150', 'Lunch', 'Vegetarian'),
            (2, 'Chicken Curry', '200', 'Dinner', 'Non-Vegetarian')
        ]
        response = {'status': 'success', 'message': 'Cafeteria Menu:', 'menu': menu, 'columns': ["item_id", "name", "price", "availability", "category"]}
        self.admin_repository.view_all_items = Mock(return_value=response)

        result = self.admin_service.view_menu({})

        self.assertEqual(result, response)
    
    def test_view_discard_list_success(self):
        discard_list = [('Pasta', '1.5', '0.2')]
        response = {'status': 'success', 'discard_list': discard_list}
        self.admin_repository.get_discard_list = Mock(return_value=response)

        result = self.admin_service.view_discard_list({})

        self.assertEqual(result, response)
    
    def test_review_discard_list_remove_success(self):
        data = {'action': 'remove', 'item_name': 'Pasta'}
        response = {'status': 'success', 'message': 'Pasta is removed from cafeteria.', 'item_id': 1}
        self.admin_repository.remove_item_by_name = Mock(return_value=response)

        result = self.admin_service.review_discard_list(data)

        self.assertEqual(result, response)

    def test_review_discard_list_get_feedback_success(self):
        data = {'action': 'get_feedback', 'item_name': 'Pasta'}
        response = {'status': 'success'}
        self.admin_repository.request_feedback = Mock(return_value=response)

        result = self.admin_service.review_discard_list(data)

        self.assertEqual(result, response)

if __name__ == '__main__':
    unittest.main()
