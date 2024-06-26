from auth.auth_service import AuthService

class AuthController:
    def __init__(self):
        self.auth_service = AuthService()

    def handle_request(self, request):
        action = request['action']
        if action == 'login':
            return self.auth_service.login(request['data'])
        elif action == 'logout':
            return self.auth_service.logout(request['data'])
        else:
            return {'status': 'error', 'message': 'Invalid action'}
