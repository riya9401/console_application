import socket
import threading

class Server():
    def __init__(self):
        self.HOST = 'localhost'
        self.PORT = 65432

    def client_handler(self,client_socket):
        try:
            while True:
                request = client_socket.recv(1024).decode()
                if not request:
                    break
                response = f"{request} recieved from client"
                client_socket.send(response.encode('utf-8'))
        finally:
            client_socket.close()

    def start_server(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((self.HOST, self.PORT))
        server_socket.listen(5)
        print(f"Server started at {self.HOST}:{self.PORT}")
        
        try:
            while True:
                client_socket, addr = server_socket.accept()
                print(f"Connection from {addr}")
                client_thread = threading.Thread(target=self.client_handler, args=(client_socket,))
                client_thread.start()
        finally:
            server_socket.close()

if __name__ == "__main__":
    server = Server()
    server_state = server.start_server()
