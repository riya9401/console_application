from common.database import Database

class AuthRepository:
    def __init__(self):
        self.db = Database()

    def validate(self, user_data):
        user_id = user_data['userId']
        username = user_data['username']
        
        query = "SELECT * FROM user WHERE user_id=%s AND user_name=%s"
        result = self.db.execute_query(query, (user_id, username))
        
        if not result:
            return {'status': 'error', 'message': 'User not found'}
        return {'status': 'success', 'message': 'valid user', 'user_id': result[0][0]}
    
    def authenticate(self, user_data):
        query = "SELECT * FROM user_credential WHERE id=%s AND password=%s"
        result = self.db.execute_query(query, (user_data["userId"], user_data["password"]))
        
        if not result:
            return {'status': 'error', 'message': 'Incorrect password'}

        return {'status': 'success', 'message': 'Login successful', 'role': 'admin', 'user_id':user_data["userId"]}