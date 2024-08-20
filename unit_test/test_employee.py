import unittest
from unittest.mock import patch, MagicMock
from employee.employee_controller import EmployeeController
from employee.employee_service import EmployeeService
from employee.employee_repository import EmployeeRepository

class TestEmployeeFunctions(unittest.TestCase):

    def setUp(self):
        self.employee_controller = EmployeeController()
        self.employee_service = EmployeeService()
        self.employee_repository = EmployeeRepository()

    @patch('employee_service.EmployeeService.voteItem')
    def test_vote_for_food_item(self, mock_vote_item):
        mock_vote_item.return_value = {'status': 'success', 'message': 'Voting for item done successfully'}
        request = {'action': 'vote_for_food_item', 'data': {'item_id': 1, 'emp_id': 123}}
        response = self.employee_controller.handle_request(request)
        self.assertEqual(response['status'], 'success')

    @patch('employee_service.EmployeeService.provideFeedback')
    def test_provide_feedback(self, mock_provide_feedback):
        mock_provide_feedback.return_value = {'status': 'success', 'message': 'Feedback provided successfully'}
        request = {'action': 'provide_feedback', 'data': {'item_id': 1, 'emp_id': 123, 'rating': 5, 'feedback': 'Good', 'sentiment_score': 0.5}}
        response = self.employee_controller.handle_request(request)
        self.assertEqual(response['status'], 'success')

    @patch('employee_service.EmployeeService.getRecommendation_accToPrefrence')
    def test_get_recommendation(self, mock_get_recommendation):
        mock_get_recommendation.return_value = {'status': 'success', 'message': 'Here are the recommendations', 'columns': [], 'menu': []}
        request = {'action': 'get_recommendation_employee', 'data': {'emp_id': 123, 'menu_type': 'Lunch'}}
        response = self.employee_controller.handle_request(request)
        self.assertEqual(response['status'], 'success')

    @patch('employee_service.EmployeeService.view_menu')
    def test_view_menu(self, mock_view_menu):
        mock_view_menu.return_value = {'status': 'success', 'menu': [], 'columns': []}
        request = {'action': 'view_menu'}
        response = self.employee_controller.handle_request(request)
        self.assertEqual(response['status'], 'success')

    @patch('employee_service.EmployeeService.myTodaysOrders')
    def test_my_todays_orders(self, mock_my_todays_orders):
        mock_my_todays_orders.return_value = {'status': 'success', 'message': 'Your today\'s orders are:', 'columns': [], 'todays_orders': []}
        request = {'action': 'my_todays_orders', 'data': {'emp_id': 123}}
        response = self.employee_controller.handle_request(request)
        self.assertEqual(response['status'], 'success')

    @patch('employee_service.EmployeeService.displayRolledOutMenu')
    def test_display_rolled_out_menu(self, mock_display_rolled_out_menu):
        mock_display_rolled_out_menu.return_value = {'status': 'success', 'message': 'Items for rolled out menu', 'columns': [], 'menu': []}
        request = {'action': 'display_RolledOutMenu', 'data': {'menu_type': 'Lunch'}}
        response = self.employee_controller.handle_request(request)
        self.assertEqual(response['status'], 'success')

    @patch('employee_service.EmployeeService.saveProfile')
    def test_save_profile(self, mock_save_profile):
        mock_save_profile.return_value = {'status': 'success', 'message': 'Profile updated successfully'}
        profile_data = {
            'emp_id': 123,
            'food_type': 'Vegetarian',
            'spice_level': 'Medium',
            'preference': 'North Indian',
            'sweet_tooth': 'Yes'
        }
        request = {'action': 'save_profile', 'data': profile_data}
        response = self.employee_controller.handle_request(request)
        self.assertEqual(response['status'], 'success')

    @patch('employee_service.EmployeeService.getProfile')
    def test_get_profile(self, mock_get_profile):
        mock_get_profile.return_value = {'status': 'success', 'message': 'Profile retrieved successfully', 'profile': {}}
        request = {'action': 'get_profile', 'data': {'emp_id': 123}}
        response = self.employee_controller.handle_request(request)
        self.assertEqual(response['status'], 'success')

    @patch('employee_service.EmployeeService.getNotifications')
    def test_get_notifications(self, mock_get_notifications):
        mock_get_notifications.return_value = {'status': 'success', 'message': 'Notifications:', 'notifications': []}
        request = {'action': 'get_notifications', 'data': {'emp_id': 123}}
        response = self.employee_controller.handle_request(request)
        self.assertEqual(response['status'], 'success')

    @patch('employee_service.EmployeeService.provideFeedback_discardItem')
    def test_provide_feedback_discard_item(self, mock_provide_feedback_discard_item):
        mock_provide_feedback_discard_item.return_value = {'status': 'success', 'message': 'Feedback provided successfully'}
        feedback = {
            'data': {'emp_id': 123, 'item_name': 'Pizza'},
            '1': 'Not tasty',
            '2': 'Should be spicy',
            '3': 'Add more cheese'
        }
        request = {'action': 'provideFeedback_discardItem', 'data': feedback}
        response = self.employee_controller.handle_request(request)
        self.assertEqual(response['status'], 'success')

    @patch('employee_service.EmployeeService.clearNotification')
    def test_clear_notification(self, mock_clear_notification):
        mock_clear_notification.return_value = {'status': 'success', 'message': 'Notification cleared'}
        request = {'action': 'clear_notification', 'data': {'notification_id': 1}}
        response = self.employee_controller.handle_request(request)
        self.assertEqual(response['status'], 'success')


if __name__ == '__main__':
    unittest.main()
