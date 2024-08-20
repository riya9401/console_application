from employee.employee_repository import EmployeeRepository

class EmployeeService:
    def __init__(self):
        self.employee_repository = EmployeeRepository()

    def voteItem(self, food_item_data):
        try:
            return self.employee_repository.vote_item(food_item_data)
        except Exception as e:
            return self._error_response(f"Error voting for food item: {e}")

    def provideFeedback(self, food_item_data):
        try:
            return self.employee_repository.provide_feedback(food_item_data)
        except Exception as e:
            return self._error_response(f"Error providing feedback: {e}")
    
    def getRecommendation(self, food_item_data):
        try:
            return self.employee_repository.get_recommendation(food_item_data)
        except Exception as e:
            return self._error_response(f"Error getting recommendation: {e}")
    
    def view_menu(self):
        try:
            return self.employee_repository.view_all_items()
        except Exception as e:
            return self._error_response(f"Error viewing menu: {e}")
    
    def myTodaysOrders(self, user_request):
        try:
            return self.employee_repository.my_todays_orders(user_request)
        except Exception as e:
            return self._error_response(f"Error getting today's orders: {e}")
    
    def displayRolledOutMenu(self, food_item_data):
        try:
            return self.employee_repository.display_rolled_out_menu(food_item_data)
        except Exception as e:
            return self._error_response(f"Error displaying rolled-out menu: {e}")
    
    def saveProfile(self, profile_data):
        try:
            return self.employee_repository.save_profile(profile_data)
        except Exception as e:
            return self._error_response(f"Error saving profile: {e}")

    def getProfile(self, emp_id):
        try:
            return self.employee_repository.get_profile(emp_id)
        except Exception as e:
            return self._error_response(f"Error getting profile: {e}")

    def getRecommendation_accToPrefrence(self, food_item_data):
        try:
            return self.employee_repository.get_recommendation_with_profile(food_item_data['emp_id'], food_item_data['menu_type'], food_item_data['max_limit'])
        except Exception as e:
            return self._error_response(f"Error getting recommendation according to preference: {e}")
    
    def getNotifications(self, emp_id):
        try:
            return self.employee_repository.get_notifications(emp_id)
        except Exception as e:
            return self._error_response(f"Error getting notifications: {e}")
        
    def get_feedback_required_list(self,user):
        try:
            return self.employee_repository.get_feedback_required_list(user)
        except Exception as e:
            return self._error_response(f"Error getting discard items list that required feedbacks: {e}")
    
    def provideFeedback_discardItem(self, emp_id):
        try:
            return self.employee_repository.provide_feedback_discard_items(emp_id)
        except Exception as e:
            return self._error_response(f"Error providing feedback to discard item: {e}")
        
    def clearNotification(self, notification_id):
        try:
            return self.employee_repository.clear_notification(notification_id)
        except Exception as e:
            return self._error_response(f"Error getting notifications: {e}")

    def _error_response(self, message):
        return {
            'status': 'error',
            'message': message
        }
