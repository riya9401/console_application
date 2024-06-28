from common.database import Database

class AdminRepository:
    def __init__(self):
        self.db = Database()
        self.table_name = 'food_item'
        
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
