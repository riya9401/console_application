from common.database import Database
from datetime import datetime, timedelta

class EmployeeRepository:
    def __init__(self):
        self.db = Database()
        self.feedback = 'feedback'
        self.vote = 'vote_item'
        self.rolled_out_menu = 'daily_menu'
        self.cafeteria_menu = 'food_item'
        self.scoring = 'item_score'
        self.profile = 'employee_profile'
        self.item_description = 'item_description'
        self.notification = 'user_notification'
        self.discard_items_feedback = 'discard_item_employee_feedback'

    def save_profile(self, profile_data):
        try:
            if self.is_profile_exists(profile_data['emp_id']):
                self._update_profile(profile_data)
            else:
                self._insert_profile(profile_data)
            return {'status': 'success', 'message': 'Profile updated successfully'}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}
    
    def is_profile_exists(self, emp_id):
        query = 'SELECT profile_id FROM {} WHERE emp_id=%s;'.format(self.profile)
        profile_id = self.db.execute_query(query, params=(emp_id,))
        return profile_id != []

    def _update_profile(self, profile_data):
        query = "UPDATE {} SET food_type=%s, spice_level=%s, preference=%s, sweet_tooth=%s WHERE emp_id=%s".format(self.profile)
        self.db.execute_query(query, params=(profile_data['food_type'], profile_data['spice_level'], profile_data['preference'], profile_data['sweet_tooth'], profile_data['emp_id']))

    def _insert_profile(self, profile_data):
        query = "INSERT INTO {} (emp_id, food_type, spice_level, preference, sweet_tooth) VALUES (%s,%s,%s,%s,%s)".format(self.profile)
        self.db.execute_query(query, params=(profile_data['emp_id'], profile_data['food_type'], profile_data['spice_level'], profile_data['preference'], profile_data['sweet_tooth']))

    def get_profile(self, emp_id):
        try:
            query = "SELECT * FROM {} WHERE emp_id = %s".format(self.profile)
            result = self.db.execute_query(query, params=(emp_id,))
            return result if result else None
        except Exception as e:
            return {'status': 'error', 'message': str(e)}
    
    def vote_item(self, request_data):
        try:
            query = "INSERT INTO {} (item_id, emp_id, vote_date) VALUES (%s, %s, %s)".format(self.vote)
            next_day = datetime.now() + timedelta(days=1)
            self.db.execute_query(query, params=(request_data['item_id'], request_data['emp_id'], next_day.strftime("%Y-%m-%d")))
            message = f"Voting for {request_data['item_id']} done successfully"
            return {'status': 'success', 'message': message}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}

    def provide_feedback(self, request_data):
        try:
            query = "INSERT INTO {} (emp_id, item_id, rating, comment, sentiment, fb_date) VALUES (%s, %s, %s, %s, %s, %s)".format(self.feedback)
            self.db.execute_query(query, params=(request_data["emp_id"], request_data["item_id"], request_data["rating"], request_data["feedback"], request_data["sentiment_score"], datetime.now().strftime("%Y-%m-%d")))
            message = f"Feedback provided for item_id: {request_data['item_id']} by employee_id: {request_data['emp_id']}."
            return {'status': 'success', 'message': message}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}
    
    def get_recommendation(self, request_data):
        try:
            query = "SELECT item.item_id, item.name, CAST(score.average_rating AS CHAR), CAST(score.average_sentiment AS CHAR), item.category FROM {} item LEFT JOIN {} score ON item.item_id = score.item_id WHERE LOWER(item.availability) IN (%s, 'all') ORDER BY score.average_rating DESC, score.average_sentiment DESC;".format(self.cafeteria_menu, self.scoring)
            recommendations = self.db.execute_query(query, params=(request_data['menu_type'].lower(),))
            columns = ['item_id', 'name', 'rating', 'score', 'category']
            message = f"Here are the recommendations to order item for {request_data['menu_type']}"
            return {'status': 'success', 'message': message, 'columns': columns, 'recommendations': recommendations}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}
    
    def get_recommendation_with_profile(self, emp_id, menu_type):
        try:
            profile = self.get_profile(emp_id)
            query = "SELECT item.item_id, item.name, item_d.foodType, item_d.spiceLevel, item_d.preferenceType, CAST(score.average_rating AS CHAR), CAST(score.average_sentiment AS CHAR) FROM {} item LEFT JOIN {} score ON item.item_id = score.item_id LEFT JOIN {} item_d ON item.item_id = item_d.item_id WHERE LOWER(item.availability) IN (%s, 'all') ORDER BY score.average_rating DESC, score.average_sentiment DESC".format(self.cafeteria_menu, self.scoring, self.item_description)
            recommendations = self.db.execute_query(query, params=(menu_type.lower(),))
            if profile:
                recommendations = self._filter_recommendations_based_on_profile(recommendations, profile)
            columns = ['item_id', 'name', 'food_type', 'spice_level', 'preference', 'rating', 'score']
            message = f"Here are the recommendations for {menu_type}"
            return {'status': 'success', 'message': message, 'columns': columns, 'recommendations': recommendations}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}
    
    def _filter_recommendations_based_on_profile(self, recommendations, profile):
        def get_preference_score(item, profile):
            score = 0
            if profile[0]['food_type'] == item[2]:
                score += 3
            if profile[0]['spice_level'] == item[3]:
                score += 2
            if profile[0]['preference'] == item[4]:
                score += 1
            return score

        scored_recommendations = [(get_preference_score(item, profile), item) for item in recommendations]
        scored_recommendations.sort(key=lambda x: x[0], reverse=True)
        return [item for _, item in scored_recommendations]

    def view_all_items(self):
        try:
            query = "SELECT * FROM {};".format(self.cafeteria_menu)
            return self.db.execute_query(query)
        except Exception as e:
            return {'status': 'error', 'message': str(e)}
    
    def my_todays_orders(self, user_request):
        try:
            query = "SELECT vote.emp_id, food_item.item_id, food_item.name FROM {} vote LEFT JOIN {} food_item ON vote.item_id = food_item.item_id WHERE vote.emp_id = %s AND vote.vote_date = %s;".format(self.vote, self.cafeteria_menu)
            todays_orders = self.db.execute_query(query, params=(user_request["emp_id"], datetime.now().strftime("%Y-%m-%d")))
            columns = ['emp_id', 'item_id', 'name']
            message = f"Your today's orders are:"
            return {'status': 'success', 'message': message, 'columns': columns, 'todays_orders': todays_orders}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}
    
    def display_rolled_out_menu(self, request_data):
        try:
            query = "SELECT menu.item_id, item.name,item.price FROM {} menu LEFT JOIN {} item ON item.item_id = menu.item_id WHERE LOWER(menu.menu_category) = %s;".format(self.rolled_out_menu, self.cafeteria_menu)
            rolled_out_menu = self.db.execute_query(query,params=(request_data['menu_type'].lower(),))
            columns = ['item_id', 'name', 'price']
            message = f"Items for rolled out menu for {request_data['menu_type']}"
            return {'status': 'success', 'message': message, 'columns': columns, 'menu': rolled_out_menu}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}
    
    def get_notifications(self, emp_id):
        try:
            query = "SELECT * FROM {} WHERE user_id = %s;".format(self.notification)
            result = self.db.execute_query(query, params=(emp_id,))
            
            return {'status': 'success', 'message':'Notifications:','notifications': result}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}
        
    def clear_notification(self, notification_id):
        try:
            query = "DELETE FROM {} WHERE notify_id = %s".format(self.notification)
            self.db.execute_query(query, params=(notification_id,))
            message = f"Cleared all notifications."
            return {'status': 'success', 'message': message}
        except Exception as e:
            return {'status': 'failure', 'message': str(e)}

    def provide_feedback_discard_items(self, feedback):
        try:
            query = "INSERT INTO {} (item_name, emp_id, discard_reason, taste_suggestion, recipe_suggestion) values (%s,%s,%s,%s,%s);".format(self.discard_items_feedback)
            self.db.execute_query(query, params=(feedback['data']['item_name'],feedback['data']['emp_id'],feedback['1'],feedback['2'],feedback['3']))
            message = f"Feedback provided successfully for {feedback['data']['item_name']}."
            return {'status': 'success', 'message': message}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}
