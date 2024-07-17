from employee.employee_service import EmployeeService

class EmployeeController:
    def __init__(self):
        self.employee_service = EmployeeService()
        self.action_map = {
            'vote_for_food_item': self.employee_service.voteItem,
            'view_menu': self.employee_service.view_menu,
            'provide_feedback': self.employee_service.provideFeedback,
            'get_recommendation_employee': self.employee_service.getRecommendation_accToPrefrence,
            'my_todays_orders': self.employee_service.myTodaysOrders,
            'display_RolledOutMenu': self.employee_service.displayRolledOutMenu,
            'save_profile': self.employee_service.saveProfile,
            'get_profile': self.employee_service.getProfile,
            'get_notifications': self.employee_service.getNotifications,
            'provideFeedback_discardItem': self.employee_service.provideFeedback_discardItem
        }

    def handle_request(self, request):
        action = request.get('action')
        if not action:
            return self._error_response("Action not specified")
        
        handler = self.action_map.get(action)
        if not handler:
            return self._error_response(f"Invalid action: {action}")

        try:
            data = request.get('data', {})
            if action in ['get_profile', 'get_notifications']:
                return handler(data['emp_id'])
            return handler(data)
        except Exception as e:
            return self._error_response(f"Error handling request: {str(e)}")
    
    def _error_response(self, message):
        return {
            'status': 'error',
            'message': message
        }
