import socket
import threading
import json
from config.configuration import Settings
from admin.admin_controller import AdminController
from chef.chef_controller import ChefController
from employee.employee_controller import EmployeeController
from auth.auth_controller import AuthController

class ClientHandler:
    def __init__(self):
        self.auth_controller = AuthController()
        self.admin_controller = AdminController()
        self.chef_controller = ChefController()
        self.employee_controller = EmployeeController()
        self.handlers = {
            'validate_user': self.auth_controller.handle_request,
            'auth_user': self.auth_controller.handle_request,
            'logout': self.auth_controller.handle_request,
            'add_food_item': self.admin_controller.handle_request,
            'update_food_item': self.admin_controller.handle_request,
            'remove_food_item': self.admin_controller.handle_request,
            'get_food_items': self.admin_controller.handle_request,
            'view_menu': self.admin_controller.handle_request,
            'view_discard_list': self.admin_controller.handle_request,
            'review_discard_list': self.admin_controller.handle_request,
            'get_recommendations': self.chef_controller.handle_request,
            'rollout_menu': self.chef_controller.handle_request,
            'view_monthly_report': self.chef_controller.handle_request,
            'display_RolledOutMenu': self.employee_controller.handle_request,
            'vote_for_food_item': self.employee_controller.handle_request,
            'get_recommendation_employee': self.employee_controller.handle_request,
            'view_menu_employee': self.employee_controller.handle_request,
            'provide_feedback': self.employee_controller.handle_request,
            'my_todays_orders': self.employee_controller.handle_request,
            'save_profile': self.employee_controller.handle_request,
            'get_profile': self.employee_controller.handle_request,
            'get_notifications': self.employee_controller.handle_request,
            'provideFeedback_discardItem':self.employee_controller.handle_request,
            'clear_notification': self.employee_controller.handle_request,
        }

    def handle_client(self, client_socket):
        try:
            while True:
                request = client_socket.recv(1024).decode('utf-8')
                if not request:
                    break
                request_data = json.loads(request)
                action = request_data.get('action')
                handler = self.handlers.get(action, self.invalid_action)
                response = handler(request_data)
                response_data = json.dumps(response).encode()
                client_socket.send(json.dumps(len(response_data)).encode())
                client_socket.send(response_data)
        except Exception as e:
            print(f"Error handling client: {e}")
        finally:
            client_socket.close()

    def invalid_action(self, request_data):
        return {'status': 'error', 'message': 'Invalid action'}

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    settings = Settings()
    try:
        server.bind((settings.HOST, settings.PORT))
        server.listen(5)
        print(f"[*] Listening on {settings.HOST}:{settings.PORT}")

        while True:
            client_socket, addr = server.accept()
            print(f"[*] Accepted connection from {addr}")
            client_handler = threading.Thread(target=handle_client_wrapper, args=(client_socket,))
            client_handler.start()
    except Exception as e:
        print(f"Server error: {e}")
    finally:
        server.close()

def handle_client_wrapper(client_socket):
    handler = ClientHandler()
    handler.handle_client(client_socket)

if __name__ == "__main__":
    start_server()
