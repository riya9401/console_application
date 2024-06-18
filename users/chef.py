from utils.db import Database
from server.request_handler import RequestHandler
from users.recommendation_engine import Recommendation
class Chef():
    def __init__(self,user):
        self.item_db = Database()
        self.requestManger = RequestHandler()
        self. chef = user
    
    def displayTasks(self):
        print(f"\nHello Chef {self.chef['name']}... ")  
        print("1. View Menu Recommendation")  
        print("2. Roll Out Menu") 
        print("3. View Monthly Feedback Reports")
        print("4. Exit")
        choice  = input("Please Enter your choice here: ")
        return choice
    
    def handleTasks(self,task):
        if task == '1':
            menu = Recommendation()
            menuType = input("1. Breakfast\n2. Lunch\n3. Snacks\n4. Dinner\n select menu type from the above list: ")
            request = menu.recommendation_for_chef(menuType)
        elif task == '2':
            request = self.rollOutMenu()
        elif task == '3':
            request = self.getMonthlyFbReport()
        elif task == '4':
            print("Exiting from task list")
            return
        self.requestManger.manage_request(request)
        
    def rollOutMenu(self):
        print("1. Breakfast\n2. Lunch\n3. Snacks\n4. Dinner")
        menu = {
            'client_type': 'chef',
            'action': 'Roll out Menu',
            'menu_type': input("select menu type from the above list: "),
            'items': list(input("Enter number of items in menu: ")),
        }
        return menu
    
    def getMonthlyFbReport(self):
        pass
    