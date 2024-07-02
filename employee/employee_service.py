from employee.employee_repository import EmployeeRepository

class EmployeeService:
    def __init__(self):
        self.employee_repository = EmployeeRepository()

    def voteItem(self, food_item_data):
        # check if food item already exists
        return self.employee_repository.vote_item(food_item_data)

    def provideFeedback(self, food_item_data):
        #check if food item already exists
        return self.employee_repository.provide_feedback(food_item_data)
    
    def getRecommendation(self, food_item_data):
        # Business logic for updating a food item
        return self.employee_repository.get_recommendation(food_item_data)
    
    def view_menu(self):
        return self.employee_repository.view_all_items()
    
    def myTodaysOrders(self,user_request):
        return self.employee_repository.my_todays_orders(user_request)
    
    def displayRolledOutMenu(self,food_item_data):
        return self.employee_repository.displayRolledOutMenu(food_item_data)