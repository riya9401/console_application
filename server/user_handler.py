# from collections.abc import Iterable
from users.admin import Admin
from users.chef import Chef
from users.employee import Employee
import string

class UserHandler():
    def __init__(self, user):
        self.user = user
        self.assignTaskToUser()
        
    def assignTaskToUser(self):
        user_type = self.user["role"]
        if user_type.upper() == "ADMIN":
            self.processAdminTasks()
        elif user_type.upper() == "CHEF":
            self.processChefTasks
        elif user_type.upper() == "EMPLOYEE":
            self.processEmployeesTasks()
        else:
            print("Access denied")
        
    def processAdminTasks(self):
        admin = Admin(self.user)
        task = admin.displayTasks()
        admin.handleTasks(task)
    
    def processChefTasks(self):
        chef = Chef(self.user)
        task = chef.displayTasks()
        chef.handleTasks(task)
    
    def processEmployeesTasks(self):
        employee = Employee(self.user)
        task = employee.displayTasks()
        employee.handleTasks(task)