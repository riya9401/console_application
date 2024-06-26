import socket
from auth_client import AuthClient
from admin_client import AdminClient
from config.config import Settings

def main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    settings = Settings()
    client_socket.connect((settings.HOST, settings.PORT))

    auth_client = AuthClient(client_socket)

    role = auth_client.login()
    if role:
        if role == 'admin':
            admin_client = AdminClient(client_socket)
            admin_client.handle_admin_actions()
        # Add handling for other roles like 'chef', 'employee'

    auth_client.logout()
    client_socket.close()

if __name__ == "__main__":
    main()
