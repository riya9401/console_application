import json

class AuthClient:
    def __init__(self, client_socket):
        self.client_socket = client_socket

    def validate_login(self):
        user_id = input("Enter your User ID: ")
        username = input("Enter username: ")
        login_request = {
            "action": "validate_user",
            "data": {
                "userId": user_id,
                "username": username,
            }
        }
        try:
            self.client_socket.sendall(json.dumps(login_request).encode('utf-8'))
            response_data = self.getResponse()
            return response_data
        except Exception as e:
            print(f"Error during login: {e}")
            return None
        
    def authenticate_user(self,id):
        login_request = {
            "action": "auth_user",
            "data": {
                "userId": id,
                "password": input("Enter your password: "),
            }
        }
        try:
            self.client_socket.sendall(json.dumps(login_request).encode('utf-8'))
            response_data = self.getResponse()
            return response_data
        except Exception as e:
            print(f"Error during login: {e}")
            return None
        
    def logout(self):
        logout_request = {
            "action": "logout",
            "data": {}
        }
        self.client_socket.sendall(json.dumps(logout_request).encode())
        response_data = self.getResponse()
        print(response_data['message'])
        
    def getResponse(self):
        response_size = json.loads(self.client_socket.recv(1024).decode())
        response = b''
        chunk = ''
        while response_size:
            chunk = self.client_socket.recv(1024)
            if not chunk:
                break
            response += chunk
            response_size -= len(chunk)
        response_data = json.loads(response.decode())
        return response_data
