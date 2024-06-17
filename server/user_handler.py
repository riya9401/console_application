# from collections.abc import Iterable
from users.admin import Admin
from users.chef import Chef
from users.employee import Employee
import string

class UserHandler():
    def __init__(self, role):
        self.user_type = role
        self.assignTaskToUser()
        
    def assignTaskToUser(self):
        if self.user_type.upper() == "ADMIN":
            user = Admin()
        elif self.user_type.upper() == "CHEF":
            user = Chef()
            pass
        elif self.user_type.upper() == "EMPLOYEE":
            user = Employee()
        else:
            print("Access denied")
            
        return user
        
    def showAdminTasks(self):
        pass
    
    def displayChefTasks(self):
        pass
    
    def displayEmployeesTasks(self):
        pass