from admin.admin_repository import AdminRepository

class AdminService:
    def __init__(self):
        self.admin_repository = AdminRepository()

    def add_food_item(self, food_item_data):
        # check if food item already exists
        newItem =  self.admin_repository.add(food_item_data)
        notification = self.admin_repository.sendNotification("newItemAdded",food_item_data)
        return newItem

    def update_food_item(self, food_item_data):
        #check if food item already exists
        updatedItem = self.admin_repository.update(food_item_data)
        notification = self.admin_repository.sendNotification("itemupdated",food_item_data)
        return updatedItem
    
    def remove_food_item(self, food_item_data):
        # Business logic for updating a food item
        removedItem = self.admin_repository.remove(food_item_data)
        notification = self.admin_repository.sendNotification("itemRemoved",food_item_data)
        return removedItem
    
    def view_menu(self):
        return self.admin_repository.view_all_items()
    
    def view_discard_list(self):
        return self.admin_repository.get_discard_list()
    
    def review_discard_list(self, data):
        if data['action'] == 'remove':
            return self.admin_repository.remove_item_by_name(data['item_name'])
        elif data['action'] == 'get_feedback':
            return self.admin_repository.request_feedback(data['item_name'])