import json
import socket
from abc import ABC, abstractmethod
from pandas import DataFrame as pd_df

class Command(ABC):
    @abstractmethod
    def execute(self):
        pass
    
    def getResponse(self):
        response = b''
        response_size = json.loads(self.client_socket.recv(1024).decode())
        while response_size:
            chunk = self.client_socket.recv(1024)
            if not chunk:
                break
            response += chunk
            response_size -= len(chunk)
        response_data = json.loads(response.decode())
        return response_data

class AddFoodItemCommand(Command):
    def __init__(self, client_socket):
        self.client_socket = client_socket

    def execute(self):
        try:
            name = input("Enter food item name: ")
            price = input("Enter food item price in Rs.: ")
            availability = input("Enter item availability(Breakfast/Lunch/Dinner): ")
            category = input("Enter item category(Vegeterian/Non-Vegeterian/eggetarian): ")
            food_type = input("Enter item food type(Curries/Rice/Fast Food/Desert/Bevereges/Paratha/Dose/Others): ")
            spice_level = input("Enter item spice level(Low/Medium/High/None): ")
            preference = input("Enter item preference type(North Indian/south Indian/Others): ")

            create_request = {
                'action': 'add_food_item',
                'data': {
                    'name': name,
                    'price': price,
                    'availability': availability,
                    'category': category,
                    'food_type': food_type,
                    'spice_level': spice_level,
                    'preference': preference
                }
            }
            self.client_socket.sendall(json.dumps(create_request).encode())
            response_data = self.getResponse()
            print(response_data['message'])
        except Exception as e:
            print(f"Error adding food item: {e}")

class UpdateFoodItemCommand(Command):
    def __init__(self, client_socket):
        self.client_socket = client_socket

    def execute(self):
        try:
            item_id = int(input("Enter food item ID: "))
            item = {1 : "Item Name",
                    2 : "Price",
                    3 : "Availability",
                    4 : "Category",
                    5 : "Food Type",
                    6 : "Preference",
                    7 : "Spice Level"}
            while True:
                for property in item:
                    print(f"{property}. {item[property]}")
                field = int(input("Choose the option needed to be updated: "))
                if field in range(1, 8):
                    break
                else:
                    print("Invalid property, please choose property to be changed from the below menu....")
            update_request = {
                'action': 'update_food_item',
                'data': {
                    'id': item_id,
                    'updating_field': item[field],
                    'updating_value': input(f"Enter updated value for {item[field]}: ")
                }
            }
            self.client_socket.sendall(json.dumps(update_request).encode())
            response_data = self.getResponse()
            print(response_data['message'])
        except Exception as e:
            print(f"Error updating food item: {e}")

class RemoveFoodItemCommand(Command):
    def __init__(self, client_socket):
        self.client_socket = client_socket

    def execute(self):
        try:
            item_id = int(input("Enter food item ID: "))
            remove_request = {
                'action': 'remove_food_item',
                'data': {'id': item_id}
            }
            self.client_socket.sendall(json.dumps(remove_request).encode())
            response_data = self.getResponse()
            print(response_data['message'])
        except Exception as e:
            print(f"Error removing food item: {e}")

class ViewMenuCommand(Command):
    def __init__(self, client_socket):
        self.client_socket = client_socket

    def execute(self):
        try:
            display_request = {'action': 'view_menu','data':{}}
            self.client_socket.sendall(json.dumps(display_request).encode())
            response_data = self.getResponse()
            print(response_data['message'])
            menu = pd_df(data=response_data['menu'], columns=response_data['columns'])
            print(menu.to_string(index=False))
        except Exception as e:
            print(f"Error viewing menu: {e}")

class ViewDiscardListCommand(Command):
    def __init__(self, client_socket):
        self.client_socket = client_socket

    def execute(self):
        try:
            discard_request = {'action': 'view_discard_list'}
            self.client_socket.sendall(json.dumps(discard_request).encode())
            response_data = self.getResponse()
            if response_data['status'] == 'success':
                discard_list = pd_df(data=response_data['discard_list'], columns=["name", "avg_rating", "sentiments"])
                print("\nDiscard Menu Item List:")
                print(discard_list.to_string(index=False))
                print("\nOptions:")
                print("1. Remove the Food Item from Menu List")
                print("2. Get Detailed Feedback")
                choice = input("Enter choice: ")
                if choice == '1':
                    item_name = input("Enter the food item name to remove: ")
                    review_request = {
                        'action': 'review_discard_list',
                        'data': {'action': 'remove', 'item_name': item_name}
                    }
                elif choice == '2':
                    item_name = input("Enter the food item name to get feedback: ")
                    review_request = {
                        'action': 'review_discard_list',
                        'data': {'action': 'get_feedback', 'item_name': item_name}
                    }
                else:
                    print("Invalid choice.")
                    return
                self.client_socket.sendall(json.dumps(review_request).encode())
                response_data = self.getResponse()
                if response_data['status'] == 'success' and choice == '2':
                    print("\nNotification to be sent to users")
                else:
                    print(response_data['message'])
            else:
                print(response_data['message'])
        except Exception as e:
            print(f"Error viewing discard list: {e}")

class AdminClient:
    def __init__(self, client_socket):
        self.client_socket = client_socket
        self.actions = {
            1: "Add New Item to Cafeteria",
            2: "Update Item Info",
            3: "Remove Item from Cafeteria",
            4: "View Menu",
            5: "View Discard Menu Item List",
            6: "Log Out"
        }
        self.commands = {
            1: AddFoodItemCommand(client_socket),
            2: UpdateFoodItemCommand(client_socket),
            3: RemoveFoodItemCommand(client_socket),
            4: ViewMenuCommand(client_socket),
            5: ViewDiscardListCommand(client_socket)
        }

    def handle_admin_actions(self):
        while True:
            try:
                print("\nAdmin Action List:")
                for task in self.actions:
                    print(f"{task}. {self.actions[task]}")
                choice = int(input("Enter choice: "))
                if choice in self.commands:
                    self.commands[choice].execute()
                elif choice == 6:
                    return 'logOut'
                else:
                    print("Invalid choice.")
            except Exception as e:
                print(f"Error handling admin actions: {e}")

# Main function for testing (not part of the AdminClient class)
def main():
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect(("localhost", 23327))
        admin_client = AdminClient(client_socket)
        admin_client.handle_admin_actions()
    except Exception as e:
        print(f"Main function error: {e}")
    finally:
        client_socket.close()

if __name__ == "__main__":
    main()
