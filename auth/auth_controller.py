from auth.auth_service import AuthService

class AuthController:
    def __init__(self):
        self.auth_service = AuthService()

    def handle_request(self, request):
        action = request['action']
        if action == 'login':
            return self.auth_service.login(request['data'])
        # Add other actions
