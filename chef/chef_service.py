from chef.chef_repository import ChefRepository

class ChefService:
    def __init__(self):
        self.chef_repository = ChefRepository()

    def get_recommendation(self, food_item_data):
        # run query for calculate average rating scores
        return self.chef_repository.getMenuRecoomendation(food_item_data)

    def rollout_menu(self, food_item_data):
        #check if food item already exists
        return self.chef_repository.rollOutMenu(food_item_data)
    
    def view_monthly_report(self, food_item_data):
        # Business logic for updating a food item
        return self.chef_repository.getMonthlyFbReport(food_item_data)
    
    def view_menu(self):
        return self.chef_repository.view_all_items()