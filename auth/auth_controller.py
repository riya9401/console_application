from auth.auth_service import AuthService

class AuthController:
    def __init__(self):
        self.auth_service = AuthService()

    def handle_request(self, request):
        action = request['action']
        if action == 'validate_user':
            return self.auth_service.login_validate(request['data'])
        elif action == 'auth_user':
            return self.auth_service.login_authenticate(request['data'])
        elif action == 'logout':
            return self.auth_service.logout(request['data'])
        else:
            return {'status': 'error', 'message': 'Invalid action'}
