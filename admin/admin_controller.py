from admin.admin_service import AdminService

class AdminController:
    def __init__(self):
        self.admin_service = AdminService()

    def handle_request(self, request):
        action = request['action']
        if action == 'add_food_item':
            return self.admin_service.add_food_item(request['data'])
        elif action == 'update_food_item':
            return self.admin_service.update_food_item(request['data'])
        elif action == 'remove_food_item':
            return self.admin_service.remove_food_item(request['data'])
        elif action == 'view_menu':
            return self.admin_service.view_menu()
