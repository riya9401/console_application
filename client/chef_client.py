class ChefClient:
    def __init__(self, client_socket):
        self.client_socket = client_socket

    def handle_chef_actions(self):
        while True:
            print("Chef Menu:")
            print("1. Get Recommendations")
            print("2. Rollout Menu")
            # More options...
            choice = input("Enter choice: ")
            if choice == '1':
                self.get_recommendations()
            elif choice == '2':
                self.rollout_menu()

    def get_recommendations(self):
        request = {'action': 'get_recommendations'}
        self.client_socket.sendall(str(request).encode())
        response = self.client_socket.recv(1024)
        print(response.decode())

    def rollout_menu(self):
        menu_id = input("Enter menu ID to rollout: ")
        rollout_request = {
            'action': 'rollout_menu',
            'data': {'menu_id': menu_id}
        }
        self.client_socket.sendall(str(rollout_request).encode())
        response = self.client_socket.recv(1024)
        print(response.decode())
