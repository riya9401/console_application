class EmployeeClient:
    def __init__(self, client_socket):
        self.client_socket = client_socket

    def handle_employee_actions(self):
        while True:
            print("Employee Menu:")
            print("1. Vote for Food Item")
            print("2. View Menu")
            print("3. Provide Feedback")
            # More options...
            choice = input("Enter choice: ")
            if choice == '1':
                self.vote_for_food_item()
            elif choice == '2':
                self.view_menu()
            elif choice == '3':
                self.provide_feedback()

    def vote_for_food_item(self):
        item_id = input("Enter food item ID to vote for: ")
        vote_request = {
            'action': 'vote_for_food_item',
            'data': {'item_id': item_id}
        }
        self.client_socket.sendall(str(vote_request).encode())
        response = self.client_socket.recv(1024)
        print(response.decode())

    def view_menu(self):
        request = {'action': 'view_menu'}
        self.client_socket.sendall(str(request).encode())
        response = self.client_socket.recv(1024)
        print(response.decode())

    def provide_feedback(self):
        item_id = input("Enter food item ID to provide feedback for: ")
        feedback = input("Enter your feedback: ")
        feedback_request = {
            'action': 'provide_feedback',
            'data': {'item_id': item_id, 'feedback': feedback}
        }
        self.client_socket.sendall(str(feedback_request).encode())
        response = self.client_socket.recv(1024)
        print(response.decode())
