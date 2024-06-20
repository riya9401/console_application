from server.db_operations import Database

class Authenticator():
    def __init__(self):
        self.db = Database()
    
    def authentication(self, id):
        password = input("Enter your password: ")
        result = self.db.fetch_data(table = "user_credentials",column=("id","password"),condition = ("WHERE id = {} AND password = '{}'".format(id, password)))
        if password==result[0][1]:
            return True
        return False

    def get_user_role(self, user_id):
        query = "SELECT user_role FROM user_access WHERE user_id = %s"
        result = self.db.fetch_data(query, (user_id,))
        if result:
            return result[0][0]
        return None

    