import unittest
from unittest.mock import patch, MagicMock
from auth.auth_controller import AuthController
from auth.auth_service import AuthService
from auth.auth_repository import AuthRepository

class TestAuth(unittest.TestCase):

    @patch('auth.auth_repository.AuthRepository.validate')
    @patch('auth.auth_repository.AuthRepository.authenticate')
    def setUp(self, mock_authenticate, mock_validate):
        self.auth_controller = AuthController()
        self.mock_validate = mock_validate
        self.mock_authenticate = mock_authenticate

    def test_validate_login_admin(self):
        request = {
            'action': 'validate_user',
            'data': {
                'userId': '1',
                'username': 'admin'
            }
        }
        self.mock_validate.return_value = {'status': 'success', 'message': 'valid user', 'user': {}}
        response = self.auth_controller.handle_request(request)
        self.assertEqual(response['status'], 'success')

    def test_validate_login_chef(self):
        request = {
            'action': 'validate_user',
            'data': {
                'userId': '2',
                'username': 'chef'
            }
        }
        self.mock_validate.return_value = {'status': 'success', 'message': 'valid user', 'user': {}}
        response = self.auth_controller.handle_request(request)
        self.assertEqual(response['status'], 'success')

    def test_validate_login_employee(self):
        request = {
            'action': 'validate_user',
            'data': {
                'userId': '3',
                'username': 'employee'
            }
        }
        self.mock_validate.return_value = {'status': 'success', 'message': 'valid user', 'user': {}}
        response = self.auth_controller.handle_request(request)
        self.assertEqual(response['status'], 'success')

    def test_authenticate_login_admin(self):
        request = {
            'action': 'auth_user',
            'data': {
                'userId': '1',
                'password': 'admin_pass'
            }
        }
        self.mock_authenticate.return_value = {'status': 'success', 'message': 'Login successful', 'role': 'admin', 'user_id': '1'}
        response = self.auth_controller.handle_request(request)
        self.assertEqual(response['status'], 'success')
        self.assertEqual(response['role'], 'admin')

    def test_authenticate_login_chef(self):
        request = {
            'action': 'auth_user',
            'data': {
                'userId': '2',
                'password': 'chef_pass'
            }
        }
        self.mock_authenticate.return_value = {'status': 'success', 'message': 'Login successful', 'role': 'chef', 'user_id': '2'}
        response = self.auth_controller.handle_request(request)
        self.assertEqual(response['status'], 'success')
        self.assertEqual(response['role'], 'chef')

    def test_authenticate_login_employee(self):
        request = {
            'action': 'auth_user',
            'data': {
                'userId': '3',
                'password': 'employee_pass'
            }
        }
        self.mock_authenticate.return_value = {'status': 'success', 'message': 'Login successful', 'role': 'employee', 'user_id': '3'}
        response = self.auth_controller.handle_request(request)
        self.assertEqual(response['status'], 'success')
        self.assertEqual(response['role'], 'employee')

    def test_invalid_login(self):
        request = {
            'action': 'auth_user',
            'data': {
                'userId': '4',
                'password': 'wrong_pass'
            }
        }
        self.mock_authenticate.return_value = {'status': 'error', 'message': 'Incorrect password'}
        response = self.auth_controller.handle_request(request)
        self.assertEqual(response['status'], 'error')

if __name__ == '__main__':
    unittest.main()
