from common.database import Database
from datetime import datetime, timedelta

class EmployeeRepository:
    def __init__(self):
        self.db = Database()
        self.feedback = 'feedback'
        self.vote = 'vote_item'
        self.rolledOutMenu = 'daily_menu'
        self.cafeteriaMenu = 'food_item'
        self.scoring = 'item_score'
        
    def vote_item(self, request_data):
        query = "insert into {} (item_id,emp_id,vote_date) values (%s,%s,%s)".format(self.vote)
        nxt_day = datetime.now() + timedelta(days=1)
        voting = self.db.execute_query(query,params= (request_data['item_id'],request_data['emp_id'],nxt_day.strftime("%Y-%m-%d")))
        message = f"Voting  for {request_data['item_id']} done successfully"
        
        return {'status': 'success', 'message': message}

    def provide_feedback(self, request_data):
        query = "insert into {} (emp_id,item_id,rating,comment,sentiment,fb_date) values (%s,%s,%s,%s,%s,%s)".format(self.feedback)
        feedback = self.db.execute_query(query,params=(request_data["emp_id"],request_data["item_id"],request_data["rating"],request_data["feedback"],request_data["sentiment_score"],datetime.now().strftime("%Y-%m-%d")))
        message = f"feedback provided for item_id: {request_data['item_id']} by employee_id: {request_data['emp_id']}."
        
        return {'status': 'success', 'message': message}
    
    def get_recommendation(self, request_data):
        query = "SELECT item.item_id,item.name,cast(score.average_rating as char),cast(score.average_sentiment as char),item.category from {} item left join {} score on item.item_id = score.item_id where lower(item.availability) in (%s, 'all') order by score.average_rating DESC, score.average_sentiment DESC;".format(self.cafeteriaMenu,self.scoring)
        recmd_item = self.db.execute_query(query,params=(request_data['menu_type'].lower(),))
        columns = ['item_id','name','rating','score','category']
        message = f"Here are the recommendation to order item for {request_data['menu_type']}"
        
        return {'status': 'success', 'message': message, 'column': columns, 'recommendation':recmd_item}
    
    def view_all_items(self):
        query  = "SELECT * FROM {}".format(self.cafeteriaMenu)
        menu = self.db.execute_query(query)
        message = "Cafeteria Menu:"
        coulumns = ["item_id","name","price","availability","category"]
        
        return {'status': 'success', 'message': message, 'menu': menu, "columns": coulumns}
    
    def displayRolledOutMenu(self, request_data):
        query  = "SELECT menu.menu_id,menu.item_id,item.name,item.price,item.category FROM {} menu left join {} item on menu.item_id = item.item_id where lower(menu.menu_category) = %s".format(self.rolledOutMenu,self.cafeteriaMenu)
        menu = self.db.execute_query(query,params=(request_data['menu_type'].lower(),))
        message = f"Menu for tomorrow's {request_data['menu_type']} :"
        coulumns = ["menu_id","item_id","name","price","category"]
        
        return {'status': 'success', 'message': message, 'menu': menu, "columns": coulumns}
    
    def my_todays_orders(self,user_data):
        query  = "SELECT vote.item_id,item.name FROM {} vote left join {} item on vote.item_id = item.item_id where vote.emp_id = {} and vote.vote_date = %s".format(self.vote,self.cafeteriaMenu,user_data['emp_id'])
        my_orders = self.db.execute_query(query,params=(datetime.now().strftime("%Y-%m-%d"),))
        message = "your today's orders are:"
        coulumns = ["item_id","name"]
        
        return {'status': 'success', 'message': message, 'orders': my_orders, "columns": coulumns}
