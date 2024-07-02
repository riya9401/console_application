from chef.chef_service import ChefService

class ChefController():
    def __init__(self):
        self.chef_service = ChefService()

    def handle_request(self, request):
        action = request['action']
        if action == 'get_recommendations':
            return self.chef_service.get_recommendation(request['data'])
        elif action == 'rollout_menu':
            return self.chef_service.rollout_menu(request['data'])
        elif action == 'view_monthly_report':
            return self.chef_service.view_monthly_report(request['data'])
        elif action == 'view_menu':
            return self.chef_service.view_menu(request['data'])
