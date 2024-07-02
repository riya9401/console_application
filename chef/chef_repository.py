from common.database import Database
import string

class ChefRepository:
    def __init__(self):
        self.db = Database()
        self.source_menu_table = 'food_item'
        self.daily_menu = 'daily_menu'
        self.rcmd = 'recommendation'
        self.feedback = 'feedback'
        
    def getMenuRecoomendation(self, request_data):
        # query =  "SELECT item.item_id, item.name, fb.rating AS rating, item.category FROM {} item LEFT JOIN {} fb ON fb.item_id = item.item_id WHERE LOWER(item.availability) RLIKE '{}' OR LOWER(item.availability) = 'all' UNION SELECT item.item_id, item.name, fb.rating AS rating, item.category FROM {} item RIGHT JOIN {} fb ON fb.item_id = item.item_id WHERE LOWER(item.availability) RLIKE '{}' OR LOWER(item.availability) = 'all' ORDER BY rating DESC LIMIT;".format(self.source_menu_table,self.feedback,request_data['menu_category'].lower(),self.source_menu_table,self.feedback,request_data['menu_category'].lower(),request_data['max_items'])
        query =  "SELECT item.item_id, item.name, fb.rating AS rating, item.category FROM {} item LEFT JOIN {} fb ON fb.item_id = item.item_id WHERE LOWER(item.availability) RLIKE '{}' OR LOWER(item.availability) = 'all' ORDER BY rating DESC LIMIT {};".format(self.source_menu_table,self.feedback,request_data['menu_category'].lower(),request_data['max_items'])
        rcmd_menu = self.db.execute_query(query)
        message = f"Menu recommendation for {request_data['menu_category']}"
        return {'status': 'success', 'message': message, 'recommendation': rcmd_menu}

    def rollOutMenu(self, request_data):
        self.clearRecords(self.daily_menu)
        for item in request_data['item']:
            query = "insert into {} (item_id, menu_category) values (%s,%s)".format(self.daily_menu)
            result = self.db.execute_query(query,params=(item,request_data['menu_type'].lower()))
        message = f"{request_data['menu_type']} Menu is rolled out."
        return {'status': 'success', 'message': message, 'category': request_data['menu_type']}
    
    def view_all_items(self):
        query  = "SELECT * FROM {}".format(self.source_menu_table)
        menu = self.db.execute_query(query)
        message = "Cafeteria Menu:"
        coulumns = ["item_id","name","price","availability","category"]
        return {'status': 'success', 'message': message, 'menu': menu, "columns": coulumns}
    
    def manually_design_menu(self,request_data):
        query = "select item_id,name,price,category from {} where availability RLIKE '{}' or availability = 'all'".format(self.source_menu_table,request_data['menu_type'].lower())
        menu = self.db.execute_query(query)
        columns = ['item_id', 'name', 'price', 'category']
        message = "manual design menu"
        # self.getSelectedItems()
        return {'status': 'success', 'message': message, 'menu': menu, "columns": columns}
    
    def getMonthlyFbReport(self,request_data):
        query = "SELECT DATE_FORMAT(fb.fb_date, '%Y-%m') AS month,item.item_id,item.name,AVG(fb.rating) AS average_rating FROM {} fb JOIN {} item ON item.item_id = fb.item_id WHERE DATE_FORMAT(fb.fb_date, '%Y-%m') = '{}-{}' GROUP By DATE_FORMAT(fb.fb_date, '%Y-%m'), item.item_id, fb.rating -- Include fb.rating in GROUP BY ORDER BY fb.rating DESC;".format(self.feedback,self.source_menu_table,request_data['year'],request_data['month'])
        result = self.db.execute_query(query)
        print(f"monthly report is generated for {request_data['month']}.")
        columns = ['year-month', 'item_id', 'item_name' ,'average_rating']
        message = f" monthly report for {request_data['month']}"
        return {'status': 'success', 'message': message, "columns": columns}

    def clearRecords(self,table_name):
        query  = 'truncate table {}'.format(table_name)
        result = self.db.execute_query(query)
        return result