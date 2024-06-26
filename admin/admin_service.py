from admin.admin_repository import AdminRepository

class AdminService:
    def __init__(self):
        self.admin_repository = AdminRepository()

    def add_food_item(self, food_item_data):
        # Business logic for creating a food item
        return self.admin_repository.add(food_item_data)

    def update_food_item(self, food_item_data):
        # Business logic for updating a food item
        return self.admin_repository.update(food_item_data)
    
    def remove_food_item(self, food_item_data):
        # Business logic for updating a food item
        return self.admin_repository.remove(food_item_data)
