import socket
import threading
import json
from config.configuration import Settings
from admin.admin_controller import AdminController
# from chef.chef_controller import ChefController
# from employee.employee_controller import EmployeeController
from auth.auth_controller import AuthController

def handle_client(client_socket):
    try:
        auth_controller = AuthController()
        admin_controller = AdminController()
        # chef_controller = ChefController()
        # employee_controller = EmployeeController()

        while True:
            request = client_socket.recv(1024).decode('utf-8')
            if not request:
                break
            request_data = json.loads(request)
            action = request_data['action']
            if action in ['validate_user','auth_user','logout']:
                response = auth_controller.handle_request(request_data)
            elif action in ['add_food_item', 'update_food_item', 'remove_food_item', 'get_food_items', 'view_menu']:
                response = admin_controller.handle_request(request_data)
            # elif action == 'get_recommendations' or action == 'rollout_menu':
            #     response = chef_controller.handle_request(request_data)
            # elif action == 'vote_for_food_item' or action == 'view_menu' or action == 'provide_feedback':
            #     response = employee_controller.handle_request(request_data)
            else:
                response = {'status': 'error', 'message': 'Invalid action'}
            client_socket.send(json.dumps(response).encode())
    except Exception as e:
        print(f"Error handling client: {e}")
    finally:
        client_socket.close()
        # pass

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
