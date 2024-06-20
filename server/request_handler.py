import json
from server.db_operations import Database
from users.client import UserClient
from users.recommendation_engine import Recommendation
import pandas as pd
from datetime import datetime

class RequestHandler():
    def __init__(self):
        self.db = Database()
        self.request_data = None
        self.action = None
        self.client = UserClient()
        self.recmd = Recommendation()
        
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
            message = f"{self.request_data['item_name']} is added to cafeteria with pirce {self.request_data['item_price']} and is available in {self.request_data['availability']}."
            
        elif self.action == 'update_item':
            if self.request_data['updating_field'] == "Item Name":
                column = "name"
            elif self.request_data['updating_field'] == "Price":
                column = "price"
            elif self.request_data['updating_field'] == "Availability":
                column = "availability"
            elif self.request_data['updating_field'] == "Category":
                column  = "category"
                itemName = self.db.fetchData(table='food_item',column='name',condition = "item_id = {}".format(self.request_data['item_id']))
            query = 'UPDATE food_item SET `{}` = %s WHERE item_id = %s'.format(column)
            item = self.db.execute_query(query,params=(self.request_data['updating_value'],self.request_data['item_id']))
            message = f"{itemName[0][0]}'s {column} is updated to {self.request_data['updating_value']}."
            
        elif self.action == "remove_item":
            itemName = self.db.fetchData(table='food_item',column='name',condition = "item_id = {}".format(self.request_data['item_id']))
            query = "DELETE FROM food_item where item_id = %s"
            item = self.db.execute_query(query,params=(self.request_data['item_id'],))
            message = f"{itemName[0][0]} is removed from cafeteria."
            
        self.client.send_notification(message)
        return json.dumps({'status': 'success', 'message': message})
            
    def handle_chef_request(self):
        if self.action == 'manually_design_menu':
            query = "select item_id,name,price,category from food_item where availability RLIKE '{}' or availability = 'all'".format(self.request_data['menu_type'].lower())
            menu = self.db.execute_query(query)
            columns = ['item_id', 'name', 'price', 'category']
            df = pd.DataFrame(menu, columns=columns)
            print(f"\nMenu:\n{df}")
            self.getSelectedItems()
            return True
            
        elif self.action == 'view_recommendation':
            menu = self.request_data['menu_items']
            columns = ['item_id', 'name', 'rating', 'category']
            df = pd.DataFrame(menu, columns=columns)
            print(f"\n{self.request_data['menu_type']} menu in Recommended item order:\n{df}")
            return True
            
        elif self.action == 'menu_rollOut':
            for item in self.request_data['selected_items']:
                query = "insert into daily_menu (item_id, menu_category) values (%s,%s)"
                result = self.db.execute_query(query,params=(item,self.request_data['menu_type']))
            message = f"{self.request_data['menu_type']} Menu is rolled out."
            self.client.send_notification(message)
            return result
        
        elif self.action == 'view_report':
            query = "SELECT DATE_FORMAT(fb.fb_date, '%Y-%m') AS month,item.item_id,item.name,AVG(fb.rating) AS average_rating FROM feedback fb JOIN food_item item ON item.item_id = fb.item_id WHERE DATE_FORMAT(fb.fb_date, '%Y-%m') = '{}-{}' GROUP By DATE_FORMAT(fb.fb_date, '%Y-%m'), item.item_id, fb.rating -- Include fb.rating in GROUP BY ORDER BY fb.rating DESC;".format(self.request_data['year'],self.request_data['month'])
            result = self.db.execute_query(query)
            print(f"monthly report is generated for {self.request_data['month']}.")
            columns = ['year-month', 'item_id', 'item_name' ,'average_rating']
            df = pd.DataFrame(result, columns=columns)
            print(df)
            return True

    def handle_employee_request(self):
        if self.action == 'vote_item':
            if self.viewRolledOutMenu():
                vote_item = self.voteItemFromRolledOutMenu()
                
            # if len(menu_options) <1:
            #     message = "menu not found"
        elif self.action == "view_menu":
            pass
        elif self.action == "provide_feedback":
            pass
        elif self.action == "my_orders":
            pass
        
        def viewRolledOutMenu(self):
            query = "select dm.item_id,item.name,item.price from daily_menu dm LEFT join food_item item on dm.item_id = item.item_id where dm.menu_category = '{}' ".format(self.request_data['menu_type'])
            rolledOutMenu = self.db.execute_query(query)
            columns = ["item_id","item_name","price"]
            df = pd.DataFrame(rolledOutMenu,columns)
            print(df)
            return True
        
        def voteItemFromRolledOutMenu(self):
            pass

    def handle_recommendation_request(self):
        query = "select"
        
    
    