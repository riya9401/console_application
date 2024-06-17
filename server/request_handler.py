import json
from server.db_operations import Database
from users.client import UserClient

class RequestHandler():
    def __init__(self):
        self.db = Database()
        self.request_data = None
        self.action = None
        self.client = UserClient()
        
    def manage_request(self,request):
        try:
            request = json.dumps(request)
            self.request_data = json.loads(request)
            client_type = self.request_data['client_type']
            self.action = self.request_data['action']
            
            if client_type == 'admin':
                return self.handle_admin_request()
            elif client_type == 'chef':
                return self.handle_chef_request()
            elif client_type == 'employee':
                return self.handle_employee_request()
            elif client_type == 'recommendation_engine':
                return self.handle_recommendation_request()
            else:
                return json.dumps({'status': 'error', 'message': 'Unknown client type'})
        finally:
            self.db.close()

    def handle_admin_request(self):
        if self.action == 'add_item':
            query = "INSERT INTO food_item (name,price,availability,category) values (%s,%s,%s,%s)"
            item = self.db.execute_query(query,params=(self.request_data['item_name'],self.request_data['item_price'],self.request_data['availability'],self.request_data['category']))
            message = f"{self.request_data['item_name']} added to Cafeteria."
            
        elif self.action == 'update_item':
            if self.request_data['field'] == "1":
                column = "name"
            elif self.request_data['field'] == "2":
                column = "price"
            elif self.request_data['field'] == "3":
                column = "availability"
            elif self.request_data['field'] == "4":
                column  = "category"
            query = "UPDATE food_item SET %s = %s WHERE item_id = %s"
            item = self.db.execute_query(query,params=(column,self.request_data['updating_value'],self.request_data['item_id']))
            itemName = ("SELECT name from food_item where item_id = %s",self.request_data['item_id'])
            message = f"{itemName[1]} is updates by {column} as {self.request_data['updating_value']}"
            
        elif self.action == "remove_item":
            query = "DELETE FROM food_item where item_id = %s"
            item = self.db.execute_query(query,params=(self.request_data['item_id']))
            itemName = ("SELECT name from food_item where item_id = %s",self.request_data['item_id'])
            message = f"{itemName} is removed from the cafeteria menu."
            
        self.client.send_notification(message)
            

    def handle_chef_request(self):
        pass

    def handle_employee_request(self):
        # Implement employee request handling logic here
        pass

    def handle_recommendation_request(db, action, data):
        # Implement recommendation engine request handling logic here
        pass
