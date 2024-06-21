import socket
import json

class UserClient():
    def __init__(self):
        self.host = 'localhost'
        self.port = 2337
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((self.host, self.port))

    def send_request(self, request):
        try:
            self.client_socket.send(request.encode('utf-8'))
            response = self.client_socket.recv(1024).decode('utf-8')
            print(f"Server response: {response}")
            
        except Exception as e:
            print(f"Error sending notification: {e}")
        
    def close(self):
        self.client_socket.close()
    
