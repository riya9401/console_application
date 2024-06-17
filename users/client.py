import socket

class UserClient():
    def __init__(self):
        self.host = 'localhost'
        self.port = 65432
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((self.host, self.port))

    def send_request(self, request):
        self.client_socket.sendall(request.encode())
        response = self.client_socket.recv(1024)
        return response.decode()
    
    def send_notification(self,message):
        self.client_socket.send(message.encode('utf-8'))
        response = self.client_socket.recv(1024).decode('utf-8')
        print(f"Server response: {response}")
        self.client_socket.send("disconnect".encode('utf-8'))
        
    def close(self):
        self.client_socket.close()
