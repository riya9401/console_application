from auth.auth_repository import AuthRepository

class AuthService:
    def __init__(self):
        self.auth_repository = AuthRepository()

    def login(self, login_data):
        user = {"user_id": login_data["userId"],
                "name": login_data["username"],
                "columns": "user_id, user_name",
                "table": "user",
                }
        return user
    
    def __is_authenticateUser(self):
        return self.__authenticator.authentication(self.login_id)
    
    def processLogin(self):
        self.__get_loginCredentials()
        if self.__validateUser():
            if self.__is_authenticateUser():
                self.login()
                # print("Login successful!")
                user_type = self.__authenticator.get_user_role(self.login_id)
                user = {"user_id": self.login_id,
                        "name": self.login_name,
                        "role": user_type}
                return user
            else:
                print("Invalid password.")
        else:
            print("Invalid login id or name")

