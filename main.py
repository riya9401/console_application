# import socket
# import threading
# import json
# from requestHandler import RequestHandler
# from config.config import Settings
# from admin.admin_controller import AdminController
# from chef.chef_controller import ChefController
# from employee.employee_controller import EmployeeController
# from auth.auth_controller import AuthController

# def handle_client(client_socket):
#     try:
#         while True:
#             request = client_socket.recv(1024).decode()
#             if not request:
#                 break
#             requset_handler = RequestHandler()
#             response = requset_handler.handle_request(request)
#             client_socket.send(response.encode('utf-8'))
#     except Exception as e:
#         print(f"Error handling client: {e}")
#     finally:
#         client_socket.close()

# def start_server():
#     server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     settings = Settings()
#     server.bind((settings.HOST, settings.PORT))
#     server.listen(5)
#     print(f"[*] Listening on {settings.HOST}:{settings.PORT}")

#     while True:
#         client_socket, addr = server.accept()
#         print(f"[*] Accepted connection from {addr}")
#         client_handler = threading.Thread(target=handle_client, args=(client_socket,))
#         client_handler.start()

# if __name__ == "__main__":
#     start_server()

import socket
import threading
import json
from config.config import Settings
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
            request = client_socket.recv(1024).decode()
            if not request:
                break
            request_data = json.loads(request)
            action = request_data['action']
            if action == 'login':
                response = auth_controller.handle_request(request_data)
            elif action.startswith('create_food_item') or action.startswith('update_food_item'):
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

if __name__ == "__main__":
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    setting = Settings()
    server.bind((setting.HOST, setting.PORT))
    server.listen(5)
    print(f"[*] Listening on {setting.HOST}:{setting.PORT}")

    while True:
        client_socket, addr = server.accept()
        print(f"[*] Accepted connection from {addr}")
        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()
