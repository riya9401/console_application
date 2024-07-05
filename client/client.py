import socket
from admin_client import AdminClient
from auth_client import AuthClient
from chef_client import ChefClient
from employee_client import EmployeeClient
# from config.configuration import Settings

def main():
    # pass
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # settings = Settings()
    client_socket.connect(("localhost", 23327))

    auth_client = AuthClient(client_socket)
    is_validUser = auth_client.validate_login()
    if is_validUser['status'] == 'success':
        authenticate_status = auth_client.authenticate_user(is_validUser['user'][0][0])
        print(f"{authenticate_status['role']} {authenticate_status['message']}")
        user = {
            'user_id': is_validUser['user'][0][0],
            'name': is_validUser['user'][0][1],
            'role': authenticate_status['role'].lower()
        }
        if user['role'] == 'admin':
            admin_client = AdminClient(client_socket)
            if admin_client.handle_admin_actions() == 'logOut':
                logoutStatus = auth_client.logout()
        elif user['role'] == 'chef':
            chef = ChefClient(client_socket)
            if chef.handle_chef_actions() == 'logOut':
                logoutStatus = auth_client.logout()
        elif user['role'] == 'employee':
            employee = EmployeeClient(client_socket,user)
            if employee.handle_employee_actions() == 'logOut':
                logoutStatus = auth_client.logout()
        else:
            return None

    # auth_client.logout()
    # client_socket.close()

if __name__ == "__main__":
    main()