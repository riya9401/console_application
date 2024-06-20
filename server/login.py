from server.Authenticator import Authenticator
from server.db_operations import Database
from server.request_handler import RequestHandler
from users.client import UserClient

class Login:
    def __init__(self):
        self.login_id = None
        self.login_name = None
        self.db = Database()
        self.__authenticator = Authenticator()
        self.client = UserClient()
        
    def __get_loginCredentials(self):
        self.login_id = int(input("Enter your Employee Id: "))
        self.login_name = input("Enter your name: ")
        
    def __validateUser(self): 
        request = {
                "request_type": "validate_user",
                "login_id": self.login_id,
                "login_name": self.login_name
            }
        return self.client.send_request(request)
        
    def __is_authenticateUser(self):
        request = {
            "request_type": "authenticate_user",
            "user_id": self.login_id,
            "password": input("Enter your password: ")
        }
        return self.client.send_request(request)
            
    def processLogin(self):
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
            
    def setLoginRequest(self):
        request = {
            "login_id": int(input("Enter your Employee Id: ")),
            "login_name": input("Enter your name: ")
        }
        return request
        
            