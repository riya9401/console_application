from common.database import Database

class AuthRepository:
    def __init__(self):
        self.db = Database()

    def get_user(self, username, password):
        # Database logic for getting user
        pass

    def __validateUser(self): 
        result = self.db.execute_query(query = "select user_id, user_name from user WHERE user_id = %s AND user_name = %s",params=(self.login_id, self.login_name.upper()))
        if result:
            return True
        return False