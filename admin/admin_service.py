from admin.admin_repository import AdminRepository

class AdminService:
    def __init__(self, admin_repository=None):
        self.admin_repository = admin_repository if admin_repository else AdminRepository()

    def add_food_item(self, food_item_data):
        try:
            new_item = self.admin_repository.add(food_item_data)
            self.admin_repository.send_notification("newItemAdded", food_item_data)
            return new_item
        except Exception as e:
            print(f"Error adding food item: {e}")
            return {'status': 'error', 'message': str(e)}

    def update_food_item(self, food_item_data):
        try:
            updated_item = self.admin_repository.update(food_item_data)
            self.admin_repository.send_notification("itemupdated", food_item_data)
            return updated_item
        except Exception as e:
            print(f"Error updating food item: {e}")
            return {'status': 'error', 'message': str(e)}

    def remove_food_item(self, food_item_data):
        try:
            removed_item = self.admin_repository.remove(food_item_data)
            self.admin_repository.send_notification("itemRemoved", food_item_data)
            return removed_item
        except Exception as e:
            print(f"Error removing food item: {e}")
            return {'status': 'error', 'message': str(e)}

    def view_menu(self,food_item_data):
        try:
            return self.admin_repository.view_all_items()
        except Exception as e:
            print(f"Error viewing menu: {e}")
            return {'status': 'error', 'message': str(e)}

    def view_discard_list(self,food_item_data):
        try:
            return self.admin_repository.get_discard_list()
        except Exception as e:
            print(f"Error viewing discard list: {e}")
            return {'status': 'error', 'message': str(e)}

    def review_discard_list(self, data):
        try:
            if data['action'] == 'remove':
                result = self.admin_repository.remove_item_by_name(data['item_name'])
            elif data['action'] == 'get_feedback':
                result = self.admin_repository.request_feedback(data['item_name'])
            else:
                result = {'status': 'error', 'message': 'Invalid action'}
            return result
        except Exception as e:
            print(f"Error reviewing discard list: {e}")
            return {'status': 'error', 'message': str(e)}

# Example usage
if __name__ == "__main__":
    service = AdminService()
    print(service.add_food_item({'name': 'Pizza', 'price': 10.99}))
    print(service.view_menu())
