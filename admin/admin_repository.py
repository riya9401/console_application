from common.database import Database
import json

class AdminRepository:
    def __init__(self):
        self.db = Database()
        self.table_name = 'food_item'
        self.feedback = 'feedback'
        self.notification = 'user_notification'
        
    def add(self, food_item_data):
        query = "insert into {} (name,price,availability,category) values(%s,{},%s,%s)".format(self.table_name,food_item_data['price'])
        result = self.db.execute_query(query, params=(food_item_data['name'],food_item_data['availability'],food_item_data['category']))
        
        if not result:
            query = "select item_id from {} where name = %s and price = {} and availability= %s and category=%s".format(self.table_name,food_item_data['price'])
            result = self.db.execute_query(query, params=(food_item_data['name'],food_item_data['availability'],food_item_data['category']))
        
        return {'status': 'success', 'message': 'item added successfully', 'item_id': result[0][0]}

    def update(self, food_item_data):
        update_type = food_item_data['updating_field']
        if update_type == "Item Name":
            column = "name"
        elif update_type == "Price":
            column = "price"
        elif update_type == "Availability":
            column = "availability"
        elif update_type == "Category":
            column  = "category"
        itemName = self.db.execute_query(query='select name from {} where item_id = {}'.format(self.table_name,food_item_data['id']))
        query = 'UPDATE {} SET `{}` = %s WHERE item_id = %s'.format(self.table_name,column)
        item = self.db.execute_query(query,params=(food_item_data['updating_value'],int(food_item_data['id'])))
        message = f"{itemName[0][0]}'s {column} is updated to {food_item_data['updating_value']}."
        return {'status': 'success', 'message': message, 'item_id': food_item_data['id']}
    
    def remove(self, food_item_data):
        itemName = self.db.execute_query(query='select name from {} where item_id = {}'.format(self.table_name,food_item_data['id']))
        query = "DELETE FROM {} where item_id = %s".format(self.table_name,)
        item = self.db.execute_query(query,params=(food_item_data['id'],))
        message = f"{itemName[0][0]} is removed from cafeteria."
        return {'status': 'success', 'message': message, 'item_id': food_item_data['id']}
    
    def view_all_items(self):
        query  = "SELECT * FROM {}".format(self.table_name)
        menu = self.db.execute_query(query)
        message = "Cafeteria Menu:"
        coulumns = ["item_id","name","price","availability","category"]
        return {'status': 'success', 'message': message, 'menu': menu, "columns": coulumns}
    
    def get_discard_list(self):
        query = f"""
        SELECT item.name, cast(AVG(fb.rating) as char) as avg_rating, GROUP_CONCAT(fb.comment SEPARATOR ', ') as sentiments
        FROM {self.table_name} item
        JOIN {self.feedback} fb ON item.item_id = fb.item_id
        GROUP BY item.name
        HAVING avg_rating < 2 OR sentiments LIKE '%Tasteless%' OR sentiments LIKE '%extremely bad experience%' OR sentiments LIKE '%very poor%';
        """
        discard_items = self.db.execute_query(query)
        return {'status': 'success', 'discard_list': discard_items}
    
    def remove_item_by_name(self, item_name):
        item = self.db.execute_query(query='select item_id from {} where name = %s'.format(self.table_name), params=(item_name,))
        if item:
            return self.remove({'id': item[0][0]})
        return {'status': 'error', 'message': 'Item not found'}
    
    def request_feedback(self, item_name):
        message = f"We are trying to improve your experience with {item_name}. Please provide your feedback and help us.\n"
        employee =self.getAllEmployeesIds()
        for employee_id in range(len(employee)):
            query  ="insert into {} (notify_type,user_id,notification,item_name) values ('feedback_required',%s,%s,%s);".format(self.notification) 
            self.db.execute_query(query,params=(employee[employee_id][0],message,item_name))
        return {'status': 'success'}
    
    def getAllEmployeesIds(self):
        query = "select user_id from user_access where lower(user_role)='employee';"
        return self.db.execute_query(query)
