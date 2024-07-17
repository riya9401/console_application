import socket
from admin_client import AdminClient
from auth_client import AuthClient
from chef_client import ChefClient
from employee_client import EmployeeClient

def main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(("localhost", 23327))
    isExit = False
    while not isExit:
        choice = int(input("1. Login\n2. Exit\n Enter your choice here: "))
        if choice == 2:
            isExit = True
            continue
        elif choice == 1:
            process_login(client_socket)
        else:
            print("Invalid choice\n Please try again....")
        
        
def process_login(client_socket):
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

if __name__ == "__main__":
    main()