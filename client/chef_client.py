import json
from datetime import datetime
from pandas import DataFrame as pd_df

class ChefClient:
    def __init__(self, client_socket):
        self.client_socket = client_socket
        self.action = {
            1: "View Menu Recommendation",
            2 : "Roll Out Menu",
            3 : "View Monthly Feedback Reports",
            4 : "Log Out"}
        self.menu_category = {
            1 : "Breakfast",
            2 : "Lunch",
            3 : "Dinner"}

    def handle_chef_actions(self):
        while True:
            print(f"\nHello Chef... ")  
            for task in self.action:  
                print(f"{task}. {self.action[task]}") 
            choice = input("Please Enter your choice here: ")
            if choice == '1':
                self.get_recommendations()
            elif choice == '2':
                self.rollout_menu()
            elif choice == '3':
                self.getMonthlyFbReport()
            elif choice == '4':
                return 'logOut'

    def get_recommendations(self):
        while True:
            for category in self.menu_category:  
                print(f"{category}. {self.menu_category[category]}") 
            print(f"{len(self.menu_category)+1}. Back to action menu")
            choice = int(input("Please enter your menu category here: "))
            if choice == len(self.menu_category)+1:
                return True
            max_item = int(input("Enter number of items in recommendate menu: "))
            request = {
                'action': 'get_recommendations',
                'data': {
                    'menu_category': self.menu_category[choice],
                    'max_items': max_item
                }
                }
            self.client_socket.sendall(json.dumps(request).encode())
            response_data = self.getResponse()
            menu = pd_df(data=response_data['recommendation'],columns=["item_id","name","rating","category"])
            print(f"{response_data['message']}\n {menu.to_string(index=False)}")
            

    def rollout_menu(self):
        while True:
            for category in self.menu_category:  
                print(f"{category}. {self.menu_category[category]}") 
            print(f"{len(self.menu_category)+1}. Back to action menu")
            choice = int(input("select menu type from the above list: "))
            if choice == len(self.menu_category)+1:
                return True
            menuType = self.menu_category[choice]
            items = []
            action = 'y'
            while action != 'n':
                items.append(int(input("Enter item ID to rollout: ")))
                action = input("Do you want to select more item? (y/n): ").lower()
            rollout_request = {
                'action': 'rollout_menu',
                'data': {
                    'menu_type': menuType,
                    'item': items}
            }
            self.client_socket.sendall(json.dumps(rollout_request).encode())
            response_data = self.getResponse()
            print(response_data['message'])

    def getMonthlyFbReport(self):
        while True:
            month = input("Enter month(number between 01 to 12): ")
            if month.isdigit() and 1 <= int(month) <= 12:
                break
            print("invalid value for month")
        monthlyReport_request = {
            'action': 'view_monthly_report',
            'year': datetime.now().year,
            "month": month,
        }
        self.client_socket.sendall(json.dumps(monthlyReport_request).encode())
        response_data = self.getResponse()
        print(response_data['message'])
        
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
    