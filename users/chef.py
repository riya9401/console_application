from server.db_operations import Database
from server.request_handler import RequestHandler
from users.recommendation_engine import Recommendation
import pandas as pd
from datetime import datetime
class Chef():
    def __init__(self,user):
        self.item_db = Database()
        self.requestManger = RequestHandler()
        self.chef = user
        self.tasks = {1: "View Menu Recommendation",
                      2 : "Roll Out Menu",
                      3 : "View Monthly Feedback Reports",
                      4 : "back"}
        
        self.menus = {1 : "Breakfast",
                      2 : "Lunch",
                      3 : "Dinner"}
    
    def displayTasks(self):
        print(f"\nHello Chef {self.chef['name']}... ")  
        for task in self.tasks:  
            print(f"{task}. {self.tasks[task]}") 
        choice  = input("Please Enter your choice here: ")
        return choice
    
    def handleTasks(self,task):
        if task == '1':
            request = self.getMenuRecoomendation()
        elif task == '2':
            request = self.rollOutMenu()
        elif task == '3':
            request = self.getMonthlyFbReport()
        elif task == '4':
            print("Exiting from task list")
            return False
        if request:
            return self.requestManger.manage_request(request)
        return False
        
    def getMenuRecoomendation(self):
        print()
        for menu_num in self.menus:  
            print(f"{menu_num}. {self.menus[menu_num]}") 
        menu = Recommendation()
        menuType = self.menus[int(input("select menu type from the above list: "))]
        recmd_menu = menu.recommend_to_chef(menuType)
        if len(recmd_menu)<1:
            rcmd_menu = self.manuallyDesignMenu(menuType)
        request  = {
        'client_type': 'chef',
        'action': 'view_recommendation',
        'menu_type': menuType,
        'menu_items': recmd_menu
        }
        return request
                   
    def manuallyDesignMenu(self,menuType):
        request = {
            'client_type': 'chef',
            'action': 'manually_design_menu',
            'menu_type': menuType
        }
        return self.requestManger.manage_request(request)
        
    def rollOutMenu(self):
        for menu_num in self.menus:  
            print(f"{menu_num}. {self.menus[menu_num]}") 
        menuType = self.menus[int(input("select menu type from the above list: "))]
        items = []
        action = 'y'
        while action != 'n':
            items.append(int(input("Enter item_id for the selected dish: ")))
            action = input("Do you want to select more item? (y/n): ").lower()
        request = {
            'client_type': 'chef',
            'action': 'menu_rollOut',
            'menu_type': menuType,
            'selected_items': items,
        }
        return self.requestManger.manage_request(request)
    
    def getMonthlyFbReport(self):
        while True:
            month = input("Enter month(number between 01 to 12): ")
            if month.isdigit() and 1 <= int(month) <= 12:
                break
            print("invalid value for month")
        report = {
            'client_type': 'chef',
            'action': 'view_report',
            'year': datetime.now().year,
            "month": month,
        }
        return report
    