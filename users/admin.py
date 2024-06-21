from server.db_operations import Database
from server.request_handler import RequestHandler

class Admin():
    def __init__(self,user):
        self.item_db = Database()
        self.requestManger = RequestHandler()
        self.admin = user
        self.tasks = {1: "Add New Item to Cafeteria ",
                      2 : "Update Item Info",
                      3 : "Remove Item from Cafeteria",
                      4 : "Log Out"}
        
        
    def displayTasks(self):
        print(f"\nHello {self.admin['name']}... \n")
        for task in self.tasks:  
            print(f"{task}. {self.tasks[task]}") 
        choice  = input("Please Enter your choice here: ")
        return choice
    
    def handleTasks(self,task):
        if task == '1':
            request = self.add_item()
        elif task == '2':
            request = self.update_item()
        elif task == '3':
            request = self.remove_item()
        elif task == '4':
            request = self.logout()
        return self.requestManger.manage_request(request)
        
        
    def add_item(self):
        request_data = {
            'client_type': 'admin',
            'action': 'add_item',
            'item_name': input("Enter name of item: "),
            'item_price': input("Enter price: "),
            'availability': input("Enter Item availability: "),
            'category': input("Enter Item category: "),
        }
        return request_data
        
    def update_item(self):
        itemId = int(input("\nEnter item id need to be update: "))
        item_struct = {1 : "Item Name",
                       2 : "Price",
                       3 : "Availability",
                       4 : "Category"}
        for property in item_struct:
            print(f"{property}. {item_struct[property]}")
        field = int(input("chosse the option needed to be update: "))
        if field in range(1,5):
            request_data = {
                'client_type': 'admin',
                'action': 'update_item',
                'item_id': itemId,
                'updating_field': item_struct[field],
                'updating_value': input(f"Enter updated value for {item_struct[field]}: "),
            }
            return request_data

    def remove_item(self):
        itemId = int(input("Enter item id need to be remove: "))
        request_data = {
            'client_type': 'admin',
            'action': 'remove_item',
            'item_id': itemId,
        }
        return request_data
    
    def logout(self):
        request = {
            'client_type': 'login_logout',
            'action': 'logout',
            'user_id': self.admin["user_id"]
        }
        return request