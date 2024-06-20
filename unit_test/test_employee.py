import unittest
from unittest.mock import MagicMock, patch
from users.employee import Employee
from users.recommendation_engine import Recommendation
from server.request_handler import RequestHandler
from utils.db import Database

class TestEmployee(unittest.TestCase):
    def setUp(self):
        self.user = {'name': 'John Doe', 'id': 1}
        self.employee = Employee(self.user)

        self.employee.requestManger = MagicMock(spec=RequestHandler)
        self.employee.db = MagicMock(spec=Database)
        self.employee.sia = MagicMock()
        self.employee.sia.polarity_scores.return_value = {'compound': 0.5}

    @patch('builtins.input', side_effect=['1', '2', '3', '4'])
    def test_displayTasks(self, mock_input):
        choice = self.employee.displayTasks()
        self.assertEqual(choice, '1')
        choice = self.employee.displayTasks()
        self.assertEqual(choice, '2')
        choice = self.employee.displayTasks()
        self.assertEqual(choice, '3')
        choice = self.employee.displayTasks()
        self.assertEqual(choice, '4')

    @patch('builtins.input', side_effect=['1'])
    def test_selectOrder(self, mock_input):
        result = self.employee.selectOrder()
        self.assertEqual(result['client_type'], 'employee')
        self.assertEqual(result['action'], 'select_order')
        self.assertEqual(result['category'], 'Breakfast')

    @patch('builtins.input', side_effect=['1'])
    def test_viewMenu(self, mock_input):
        self.employee.viewMenu()
        self.employee.requestManger.manage_request.assert_called_once()
        args = self.employee.requestManger.manage_request.call_args[0][0]
        self.assertEqual(args['client_type'], 'employee')
        self.assertEqual(args['action'], 'view_menu')
        self.assertEqual(args['menu_type'], 'Breakfast')

    @patch('builtins.input', side_effect=['5', 'Great food!'])
    def test_provideFeedback(self, mock_input):
        self.employee.getOrderId = MagicMock(return_value=123)
        result = self.employee.provideFeedback()
        self.assertEqual(result['client_type'], 'employee')
        self.assertEqual(result['action'], 'provide_feedback')
        self.assertEqual(result['order_id'], 123)
        self.assertEqual(result['rating'], 5)
        self.assertEqual(result['comment'], 'Great food!')
        self.assertEqual(result['sentiment_score'], 0.5)


if __name__ == '__main__':
    unittest.main()
