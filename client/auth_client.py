import json

class AuthClient:
    def __init__(self, client_socket):
        self.client_socket = client_socket

    def login(self):
        user_id = input("Enter your User ID: ")
        username = input("Enter username: ")
        login_request = {
            "action": "login",
            "data": {
                "userId": user_id,
                "username": username,
            }
        }
        self.client_socket.sendall(json.dumps(login_request).encode())
        response = self.client_socket.recv(1024)
        response_data = response.decode()
        if response_data:
            print("waiting for authentication...")
            return self.authentication()
        else:
            print("Invalid userI or Username!")
            return None
        
    def authentication(self):
        password = input("Enter password: ")
        auth_request = {
            "action": "auth",
            "data": {
                "password": password
            }
        }
        self.client_socket.sendall(json.dumps(auth_request).encode())
        response = self.client_socket.recv(1024)
        response_data = response.decode()
        if response_data:
            print("Login successful!")
            return response_data['role']
        else:
            print("Incorrect Password!\nLogin failed!")
            return None
