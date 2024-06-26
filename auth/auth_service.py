from auth.auth_repository import AuthRepository

class AuthService:
    def __init__(self):
        self.auth_repository = AuthRepository()

    def login(self, user_data):
        return self.auth_repository.authenticate(user_data)

    def logout(self, user_data):
        # Implement logout logic if needed (e.g., session management)
        return {'status': 'success', 'message': 'User logged out successfully'}
