from server.Authenticator import Authenticator
from server.db_operations import Database
from server.request_handler import RequestHandler

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
        result = self.db.fetch_data(table = "users",column = ("user_id","user_name"),condition = ("WHERE user_id = {} AND user_name = '{}'".format(self.login_id, self.login_name.upper())))
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
                user = {"user_id": self.login_id,
                        "name": self.login_name,
                        "role": user_type}
                return user
            else:
                print("Invalid password.")
        else:
            print("Invalid login id or name")
            
            