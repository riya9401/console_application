import socket
from auth_client import AuthClient
from admin_client import AdminClient
from chef_client import ChefClient
from employee_client import EmployeeClient

class Client:
    def __init__(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect(('localhost', 23327))
        self.auth_client = AuthClient(self.client_socket)
        self.admin_client = AdminClient(self.client_socket)
        self.chef_client = ChefClient(self.client_socket)
        self.employee_client = EmployeeClient(self.client_socket)

    def run(self):
        role = self.auth_client.login()
        if role == 'admin':
            self.admin_client.handle_admin_actions()
        elif role == 'chef':
            self.chef_client.handle_chef_actions()
        elif role == 'employee':
            self.employee_client.handle_employee_actions()

if __name__ == "__main__":
    client = Client()
    client.run()
