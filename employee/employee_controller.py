from employee.employee_service import EmployeeService

class EmployeeController:
    def __init__(self):
        self.employee_service = EmployeeService()

    def handle_request(self, request):
        action = request['action']
        if action == 'vote_for_food_item':
            return self.employee_service.voteItem(request['data'])
        elif action == 'view_menu':
            return self.employee_service.view_menu()
        elif action == 'provide_feedback':
            return self.employee_service.provideFeedback(request['data'])
        elif action == 'get_recommendation_employee':
            return self.employee_service.getRecommendation(request['data'])
        elif action == 'my_todays_orders':
            return self.employee_service.myTodaysOrders(request['data'])
        elif action == 'display_RolledOutMenu':
            return self.employee_service.displayRolledOutMenu(request['data'])
