import socket
import json

class UserClient():
    def __init__(self):
        self.host = 'localhost'
        self.port = 2337
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((self.host, self.port))

    def send_request(self, request):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.host, self.port))
            s.sendall(json.dumps(request).encode('utf-8'))
            response = s.recv(1024)
            return json.loads(response.decode('utf-8'))
        
    def close(self):
        self.client_socket.close()
    
