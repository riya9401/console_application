import socket
import threading
import json
from decimal import Decimal
from config.configuration import Settings
from admin.admin_controller import AdminController
from chef.chef_controller import ChefController
from employee.employee_controller import EmployeeController
from auth.auth_controller import AuthController

class RequestHandler:
    def __init__(self):
        self.auth_controller = AuthController()
        self.admin_controller = AdminController()
        self.chef_controller = ChefController()
        self.employee_controller = EmployeeController()
        
    def handle_request(self, request):
        action = request['action']
        if action in ['validate_user', 'auth_user', 'logout']:
            response = self.auth_controller.handle_request(request)
        elif action in ['add_food_item', 'update_food_item', 'remove_food_item', 'get_food_items', 'view_menu', 'view_discard_list', 'review_discard_list']:
            response = self.admin_controller.handle_request(request)
        elif action in ['get_recommendations', 'rollout_menu']:
            response = self.chef_controller.handle_request(request)
        elif action in ['display_RolledOutMenu', 'vote_for_food_item', 'get_recommendation_employee', 'view_menu', 'provide_feedback', 'my_todays_orders', 'save_profile', 'get_profile', 'get_notifications','provideFeedback_discardItem']:
            response = self.employee_controller.handle_request(request)
        else:
            response = {'status': 'error', 'message': 'Invalid action'}
            
        return response
        
def handle_client(client_socket):
    try:
        request_handler = RequestHandler()
        while True:
            request = client_socket.recv(1024).decode('utf-8')
            if not request:
                break
            request_data = json.loads(request)
            response = request_handler.handle_request(request_data)
            client_socket.send(json.dumps(response).encode())
    except Exception as e:
        print(f"Error handling client: {e}")
        client_socket.send(json.dumps({'status': 'error', 'message': str(e)}).encode())

if __name__ == "__main__":
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    settings = Settings()
    server.bind((settings.HOST, settings.PORT))
    server.listen(5)
    print(f"[*] Listening on {settings.HOST}:{settings.PORT}")
    
    while True:
        client_socket, addr = server.accept()
        print(f"[*] Accepted connection from {addr}")
        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()
