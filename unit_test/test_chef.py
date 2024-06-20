import unittest
from unittest.mock import MagicMock, patch
from users.chef import Chef
from users.recommendation_engine import Recommendation
from server.request_handler import RequestHandler
from server.db_operations import Database

class TestChef(unittest.TestCase):
    def setUp(self):
        self.user = {'name': 'Chef John', 'id': 1}
        self.chef = Chef(self.user)

    @patch('builtins.input', side_effect=['4'])
    def test_displayTasks(self, mock_input):
        with patch('builtins.print') as mock_print:
            choice = self.chef.displayTasks()
            self.assertEqual(choice, '4')
            mock_print.assert_any_call("\nHello Chef Gordon Ramsay... ")

    @patch('builtins.input', side_effect=['2'])
    def test_getMenuRecoomendation(self, mock_input):
        recommendation_mock = MagicMock(spec=Recommendation)
        recommendation_mock.recommend_to_chef.return_value = ['Pasta', 'Salad']

        with patch('chef.Recommendation', return_value=recommendation_mock):
            request = self.chef.getMenuRecoomendation()
            self.assertEqual(request['client_type'], 'chef')
            self.assertEqual(request['action'], 'view_recommendation')
            self.assertEqual(request['menu_type'], 'Breakfast')

    @patch('builtins.input', side_effect=['1'])
    def test_no_recommendations(self, mock_input):
        recommendation_mock = MagicMock(spec=Recommendation)
        recommendation_mock.recommend_to_chef.return_value = []

        with patch('chef.Recommendation', return_value=recommendation_mock):
            request = self.chef.getMenuRecoomendation()
            self.chef.requestManger.manage_request.assert_called_once()
            self.assertEqual(request['client_type'], 'chef')
            self.assertEqual(request['action'], 'view_recommendation')
            self.assertEqual(request['menu_type'], 'Breakfast')

    @patch('builtins.input', side_effect=['2'])
    def test_rollOutMenu(self, mock_input):
        request = self.chef.rollOutMenu()
        self.assertEqual(request['client_type'], 'chef')
        self.assertEqual(request['action'], 'Roll out Menu')
        self.assertEqual(request['menu_type'], 'Lunch')

    @patch('builtins.input', side_effect=['jan'])
    def test_getMonthlyFbReport(self, mock_input):
        report = self.chef.getMonthlyFbReport()
        self.assertEqual(report['client_type'], 'chef')
        self.assertEqual(report['action'], 'view_monthly_feedback')
        self.assertEqual(report['month'], 'jan')
        self.assertEqual(report['report'], 'Monthly feedback report data...')

if __name__ == '__main__':
    unittest.main()
