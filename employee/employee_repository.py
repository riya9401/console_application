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
        self.profile = 'employee_profile'
        self.itemDescription = 'item_description'
        self.notification = 'user_notification'
        self.discardItemsFeedback = 'discard_item_employee_feedback'
    
    def save_profile(self, profile_data):
        if self.isProfileExists(profile_data['emp_id']) != []:
            query = "UPDATE {} SET food_type=%s, spice_level=%s, preference=%s, sweet_tooth=%s where emp_id=%s".format(self.profile)
            self.db.execute_query(query, params=(profile_data['food_type'],profile_data['spice_level'],profile_data['preference'],profile_data['sweet_tooth'],profile_data['emp_id']))
        else:
            query = "INSERT INTO {} (emp_id, food_type, spice_level, preference, sweet_tooth) VALUES (%s,%s,%s,%s,%s)".format(self.profile)
            self.db.execute_query(query, params=(profile_data['emp_id'],profile_data['food_type'],profile_data['spice_level'],profile_data['preference'],profile_data['sweet_tooth']))
        return {'status': 'success', 'message': 'Profile updated successfully'}
    
    def isProfileExists(self,employee):
        query = 'select profile_id from {} where emp_id=%s;'.format(self.profile)
        profileId = self.db.execute_query(query, params=(employee,))
        return profileId
    
    def get_profile(self, emp_id):
        query = "SELECT * FROM {} WHERE emp_id = %s".format(self.profile)
        result = self.db.execute_query(query, params=(emp_id,))
        if result:
            return result
        return None
    
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
    
    def get_recommendation_with_profile(self, emp_id, menu_type):
        profile = self.get_profile(emp_id)
        query = "SELECT item.item_id, item.name, item_d.foodType, item_d.spiceLevel, item_d.prefrenceType, cast(score.average_rating as char), cast(score.average_sentiment as char) FROM {} item LEFT JOIN {} score ON item.item_id = score.item_id left join {} item_d on item.item_id=item_d.item_id WHERE LOWER(item.availability) IN (%s, 'all') ORDER BY score.average_rating DESC, score.average_sentiment DESC".format(self.cafeteriaMenu, self.scoring,self.itemDescription)
        recmd_item = self.db.execute_query(query, params=(menu_type.lower(),))
        
        if profile:
            recmd_item = self.filter_recommendations_based_on_profile(recmd_item, profile)
        
        columns = ['item_id', 'name', 'food_type', 'spice_level', 'preference', 'rating', 'score']
        message = f"Here are the recommendations for {menu_type}"
        
        return {'status': 'success', 'message': message, 'column': columns, 'recommendation': recmd_item}
    
    def filter_recommendations_based_on_profile(self, recommendations, profile):
        def get_preference_score(item, profile):
            score = 0
            if item[4].lower() == profile[0][4].lower():    #preference matches
                score += 1
            if profile[0][3].lower() == item[3].lower():    #spice level matches
                score += 1
            if profile[0][2].lower() == item[2].lower():    #food type veg/non-veg/egg matches
                score += 1
            if profile[0][5].lower() == 'yes' and (item[4].lower() in ['desert',] or item[3].lower()== 'none' ):   #sweet tooth matches
                score += 1
            return score
        
        recommendations.sort(key=lambda x: get_preference_score(x, profile), reverse=True)
        return recommendations
    
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
    
    def get_notifications(self, emp_id):
        query = "SELECT * FROM {} WHERE user_id = %s".format(self.notification)
        notifications = self.db.execute_query(query, params=(emp_id,))
        columns = ["notification_id", "notification_type", "emp_id", "notification",'item_name']
        self.clearNotification(emp_id,notifications)
        return {'status': 'success', 'message': "Your notifications:", 'notification': notifications,"columns": columns}
    
    def clearNotification(self,emp,notifications):
        for notification_id in notifications:
            query  = 'DELETE FROM {} where notify_type = %s and item_name = %s and user_id = %s'.format(self.notification)
            self.db.execute_query(query,params=(notification_id[1],notification_id[4],notification_id[2]))
            
    def provideFeedback_discardItems(self, feedback):
        query = "insert into {} (item_name,emp_id,discard_reason,taste_suggestion,recipe_suggestion) values (%s,%s,%s,%s,%s)".format(self.discardItemsFeedback)
        self.db.execute_query(query,params=(feedback['data']['item_name'],feedback['data']['emp_id'],feedback['1'],feedback['2'],feedback['3']))
        return {'status': 'success', 'message': "Your feebdback got registered, Thanks you for sharing your feedback."}
