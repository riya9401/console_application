from utils.db import Database
from server.request_handler import RequestHandler

class Admin():
    def __init__(self):
        task=self.displayTasks()
        self.item_db = Database()
        self.requestManger = RequestHandler()
        self.handleTasks(task)
        
        
    def displayTasks(self):
        print("Hello Admin... ")  
        print("1. Add New Item to Cafeteria")  
        print("2. Update Item Info.") 
        print("3. Remove Item from Cafeteria")
        print("4. back.")
        choice  = input("Please Enter your choice here: ")
        return choice
    
    def handleTasks(self,task):
        if task == '1':
            request = self.add_item()
        elif task == '2':
            self.update_item()
        elif task == '3':
            self.remove_item()
        elif task == '4':
            print("Exiting from task list")
            return
        self.requestManger.manage_request(request)
        
        
    def add_item(self):
        request_data = {
            'client_type': 'admin',
            'action': 'add_item',
            'item_name': input("Enter name of item:"),
            'item_price': input("Enter price: "),
            'availability': input("Enter Item availability: "),
            'category': input("Enter Item category: "),
        }
        return request_data
        
    def update_item(self):
        itemId = input("Enter item id need to be update: ")
        field = input("chosse the option needed to be update:\n1. Item Name\n2. Price\n3. Availability\n4.Category")
        if field in range(1,5):
            request_data = {
                'client_type': 'admin',
                'action': 'update_item',
                'item_id': itemId,
                'updating_field': field,
                'updating_value': input(f"Enter updated value for {field}: "),
            }
            return request_data

    def remove_item(self):
        itemId = input("Enter item id need to be remove: ")
        request_data = {
            'client_type': 'admin',
            'action': 'remove_item',
            'item_id': itemId,
        }
        return request_data