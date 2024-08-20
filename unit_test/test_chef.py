import unittest
from unittest.mock import MagicMock, patch
from chef.chef_controller import ChefController
from chef.chef_service import ChefService
from chef.chef_repository import ChefRepository

class TestChefFunctionalities(unittest.TestCase):
    def setUp(self):
        self.chef_controller = ChefController()
        self.chef_service = ChefService()
        self.chef_repository = ChefRepository()

    def test_get_recommendations(self):
        request_data = {'menu_category': 'Lunch', 'max_items': 5}
        expected_result = {'status': 'success', 'message': 'Menu recommendation for Lunch', 'recommendation': []}
        
        self.chef_repository.getMenuRecoomendation = MagicMock(return_value=expected_result)
        
        result = self.chef_service.get_recommendation(request_data)
        self.assertEqual(result, expected_result)
        
        result = self.chef_controller.handle_request({'action': 'get_recommendations', 'data': request_data})
        self.assertEqual(result, expected_result)

    def test_rollout_menu(self):
        request_data = {'menu_type': 'Lunch', 'item': [1, 2, 3]}
        expected_result = {'status': 'success', 'message': 'Lunch Menu is rolled out.', 'category': 'Lunch'}
        
        self.chef_repository.rollOutMenu = MagicMock(return_value=expected_result)
        
        result = self.chef_service.rollout_menu(request_data)
        self.assertEqual(result, expected_result)
        
        result = self.chef_controller.handle_request({'action': 'rollout_menu', 'data': request_data})
        self.assertEqual(result, expected_result)

    def test_view_monthly_report(self):
        request_data = {'year': 2023, 'month': '07'}
        expected_result = {
            'status': 'success', 
            'message': 'monthly report for 07', 
            "columns": ['year-month', 'item_id', 'item_name' ,'average_rating'],
            'report': []
        }
        
        self.chef_repository.getMonthlyFbReport = MagicMock(return_value=expected_result)
        
        result = self.chef_service.view_monthly_report(request_data)
        self.assertEqual(result, expected_result)
        
        result = self.chef_controller.handle_request({'action': 'view_monthly_report', 'data': request_data})
        self.assertEqual(result, expected_result)

    def test_view_menu(self):
        expected_result = {
            'status': 'success', 
            'message': 'Cafeteria Menu:', 
            'menu': [], 
            "columns": ["item_id","name","price","availability","category"]
        }
        
        self.chef_repository.view_all_items = MagicMock(return_value=expected_result)
        
        result = self.chef_service.view_menu()
        self.assertEqual(result, expected_result)
        
        result = self.chef_controller.handle_request({'action': 'view_menu'})
        self.assertEqual(result, expected_result)

if __name__ == '__main__':
    unittest.main()
