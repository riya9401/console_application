import json
from pandas import DataFrame as pd_df

class AdminClient:
    def __init__(self, client_socket):
        self.client_socket = client_socket
        self.actions = {1: "Add New Item to Cafeteria ",
                      2 : "Update Item Info",
                      3 : "Remove Item from Cafeteria",
                      4 : "View Menu",
                      5 : "Log Out"}

    def handle_admin_actions(self):
        while True:
            print("\nAdmin Action List:")
            for task in self.actions:  
                print(f"{task}. {self.actions[task]}") 
            choice = input("Enter choice: ")
            if choice == '1':
                self.add_food_item()
            elif choice == '2':
                self.update_food_item()
            elif choice == '3':
                self.remove_food_item()
            elif choice == '4':
                self.view_menu()
            elif choice == '5':
                return 'logOut'

    def add_food_item(self):
        name = input("Enter food item name: ")
        price = input("Enter food item price: ")
        availability = input("Enter item availability: ")
        category = input("Enter item category: ")
        create_request = {
            'action': 'add_food_item',
            'data': {
                'name': name,
                'price': price,
                'availability': availability,
                'category': category
            }
        }
        self.client_socket.sendall(json.dumps(create_request).encode())
        response = self.client_socket.recv(1024)
        response_data = json.loads(response.decode())
        print(response_data['message'])
        
    def update_food_item(self):
        item_id = input("Enter food item ID: ")
        item = {1 : "Item Name",
                       2 : "Price",
                       3 : "Availability",
                       4 : "Category"}
        while True:
            for property in item:
                print(f"{property}. {item[property]}")
            field = int(input("chosse the option needed to be update: "))
            if field in range(1,5):
                break
            else:
                print("Invalid property, please choose property need to be change from the below menu....")
        update_request = {
            'action': 'update_food_item',
            'data': {
                'id': item_id,
                'updating_field': item[field],
                'updating_value': input(f"Enter updated value for {item[field]}: ")
            }
        }
        self.client_socket.sendall(json.dumps(update_request).encode())
        response = self.client_socket.recv(1024)
        response_data = json.loads(response.decode())
        print(response_data['message'])

    def remove_food_item(self):
        item_id = int(input("Enter food item ID: "))
        remove_request = {
            'action': 'remove_food_item',
            'data': {
                'id': item_id,}
        }
        self.client_socket.sendall(json.dumps(remove_request).encode())
        response = self.client_socket.recv(1024)
        response_data = json.loads(response.decode())
        print(response_data['message'])
        
    def view_menu(self):
        display_request = {
            'action': 'view_menu',
        }
        self.client_socket.sendall(json.dumps(display_request).encode())
        response = self.client_socket.recv(1024)
        response_data = json.loads(response.decode())
        print(response_data['message'])
        menu = pd_df(data=response_data['menu'], columns=response_data['columns'])
        print(menu.to_string(index=False))
        
        