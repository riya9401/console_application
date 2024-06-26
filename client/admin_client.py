import json

class AdminClient:
    def __init__(self, client_socket):
        self.client_socket = client_socket

    def handle_admin_actions(self):
        while True:
            print("Admin Menu:")
            print("1. add Food Item")
            print("2. Update Food Item")
            print("3. remove Food Item")
            choice = input("Enter choice: ")
            if choice == '1':
                self.add_food_item()
            elif choice == '2':
                self.update_food_item()

    def add_food_item(self):
        name = input("Enter food item name: ")
        price = input("Enter food item price: ")
        create_request = {
            'action': 'create_food_item',
            'data': {
                'name': name,
                'price': price
            }
        }
        self.client_socket.sendall(json.dumps(create_request).encode())
        response = self.client_socket.recv(1024)
        print(response.decode())

    def update_food_item(self):
        item_id = input("Enter food item ID: ")
        name = input("Enter new food item name: ")
        price = input("Enter new food item price: ")
        update_request = {
            'action': 'update_food_item',
            'data': {
                'id': item_id,
                'name': name,
                'price': price
            }
        }
        self.client_socket.sendall(json.dumps(update_request).encode())
        response = self.client_socket.recv(1024)
        print(response.decode())
