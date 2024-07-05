from admin.admin_service import AdminService

class AdminController:
    def __init__(self):
        self.admin_service = AdminService()
        self.action_map = {
            'add_food_item': self.admin_service.add_food_item,
            'update_food_item': self.admin_service.update_food_item,
            'remove_food_item': self.admin_service.remove_food_item,
            'view_menu': self.admin_service.view_menu,
            'view_discard_list': self.admin_service.view_discard_list,
            'review_discard_list': self.admin_service.review_discard_list,
            # 'get_food_item_details': self.admin_service.get_food_item_details
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
            return handler(data)
        except Exception as e:
            return self._error_response(f"Error handling request: {str(e)}")
    
    def _error_response(self, message):
        return {
            'status': 'error',
            'message': message
        }
