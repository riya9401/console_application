import socket
from admin_client import AdminClient
from auth_client import AuthClient
# from config.configuration import Settings

def main():
    # pass
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # settings = Settings()
    client_socket.connect(("localhost", 23327))

    auth_client = AuthClient(client_socket)
    is_validUser = auth_client.validate_login()
    if is_validUser['status'] == 'success':
        authenticate_status = auth_client.authenticate_user(is_validUser['user_id'])
        print(f"{authenticate_status['role']} {authenticate_status['message']}")
        if authenticate_status['role'] == 'admin':
            admin_client = AdminClient(client_socket)
            if admin_client.handle_admin_actions() == 'logOut':
                logoutStatus = auth_client.logout()
        else:
            return None
        # Add handling for other roles like 'chef', 'employee'

    # auth_client.logout()
    # client_socket.close()

if __name__ == "__main__":
    main()
