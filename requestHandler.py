
import json

class RequestHandler():
    def __init__(self,request):
        # self.db = Database()
        self.request_data = json.dumps(request)
        # self.action = None
        # self.client = UserClient()
        # self.recmd = Recommendation()
        
        def manage_request(self):
            try:
                client_type = self.request_data['client_type']
                self.action = self.request_data['action']
                
                if client_type == 'admin':
                    return self.handle_admin_request()
                # elif client_type == 'login_logout':
                #     return self.handle_login_logout_request()
                # elif client_type == 'chef':
                #     return self.handle_chef_request()
                # elif client_type == 'employee':
                #     return self.handle_employee_request()
                # elif client_type == 'recommendation_engine':
                #     return self.handle_recommendation_request()
                else:
                    return json.dumps({'status': 'error', 'message': 'Unknown client type'})
            finally:
                pass
        
# request_load = json.loads(request)
            # if request_load["action"] == "login":
            #     auth_controller = AuthController()   
            #     if auth_controller.validate(request_load["data"]["userName"], request_load["data"]["userId"]): 
            #         if auth_controller.authenticate(request_load["data"]["userId"], request_load["data"]["password"]): 
            #             response = {"status": "success", "message": "Login successful"}
            #         else:
            #             response = {"status": "error", "message": "Invalid userId or password"}
            #     else:
            #             response = {"status": "error", "message": "Invalid user Id or user name"}
            # elif request_load["action"] == "logout":
            #     pass
            # elif request_load["action"] == "update":
            #     pass
            # elif request_load["action"] == "notification":
            #     pass
            # client_socket.send(json.dumps(response).encode('utf-8'))
            # response = f'{request_load["action"]} request recieved from {request_load["data"]["userId"]}'