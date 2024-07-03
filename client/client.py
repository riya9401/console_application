import socket
from admin_client import AdminClient
from auth_client import AuthClient
from chef_client import ChefClient
from employee_client import EmployeeClient

class ClientApp:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    def connect(self):
        try:
            self.client_socket.connect((self.host, self.port))
        except Exception as e:
            print(f"Error connecting to server: {e}")
            raise

    def run(self):
        try:
            self.connect()
            auth_client = AuthClient(self.client_socket)
            is_valid_user = self.validate_user(auth_client)
            if is_valid_user:
                authenticate_status = auth_client.authenticate_user(is_valid_user['user'][0][0])
                print(f"{authenticate_status['role']} {authenticate_status['message']}")
                user = self.get_user_info(is_valid_user, authenticate_status)
                self.handle_role_actions(user, auth_client)
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            self.cleanup(auth_client)

    def validate_user(self, auth_client):
        try:
            is_valid_user = auth_client.validate_login()
            if is_valid_user['status'] != 'success':
                print("User validation failed.")
                return None
            return is_valid_user
        except Exception as e:
            print(f"Validation error: {e}")
            return None

    def get_user_info(self, is_valid_user, authenticate_status):
        return {
            'user_id': is_valid_user['user'][0][0],
            'name': is_valid_user['user'][0][1],
            'role': authenticate_status['role'].lower()
        }

    def handle_role_actions(self, user, auth_client):
        try:
            if user['role'] == 'admin':
                self.handle_admin_actions(auth_client)
            elif user['role'] == 'chef':
                self.handle_chef_actions(auth_client)
            elif user['role'] == 'employee':
                self.handle_employee_actions(auth_client, user)
            else:
                print("Unknown role.")
        except Exception as e:
            print(f"Error handling actions for role {user['role']}: {e}")

    def handle_admin_actions(self, auth_client):
        admin_client = AdminClient(self.client_socket)
        if admin_client.handle_admin_actions() == 'logOut':
            auth_client.logout()

    def handle_chef_actions(self, auth_client):
        chef_client = ChefClient(self.client_socket)
        if chef_client.handle_chef_actions() == 'logOut':
            auth_client.logout()

    def handle_employee_actions(self, auth_client, user):
        employee_client = EmployeeClient(self.client_socket, user)
        if employee_client.handle_employee_actions() == 'logOut':
            auth_client.logout()

    def cleanup(self, auth_client):
        try:
            auth_client.logout()
        except Exception as e:
            print(f"Error during logout: {e}")
        finally:
            self.client_socket.close()

if __name__ == "__main__":
    app = ClientApp(host="localhost", port=23327)
    app.run()
