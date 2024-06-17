from server.Authenticator import Authenticator
from utils.db import Database

class Login:
    def __init__(self):
        self.login_id = None
        self.login_name = None
        self.db = Database()
        self.__authenticator = Authenticator()
        
    def __get_loginCredentials(self):
        self.login_id = int(input("Enter your Employee Id: "))
        self.login_name = input("Enter your name: ")
        
    def __validateUser(self): 
        query = "SELECT * FROM users WHERE user_id = %s AND user_name = %s"
        result = self.db.fetch_data(query, (self.login_id, self.login_name.upper()))
        if result:
            return True
        return False
        
    def __is_authenticateUser(self):
        return self.__authenticator.authentication(self.login_id)
            
    def processRequest(self):
        self.__get_loginCredentials()
        if self.__validateUser():
            if self.__is_authenticateUser():
                print("Login successful!")
                user_type = self.__authenticator.get_user_role(self.login_id)
                return user_type
            else:
                print("Invalid password.")
        else:
            print("Invalid login id or name")
            
            