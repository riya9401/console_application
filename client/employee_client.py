import json
from datetime import datetime
from pandas import DataFrame as pd_df
from nltk.sentiment import SentimentIntensityAnalyzer

class EmployeeClient:
    def __init__(self, client_socket, employee_details):
        self.client_socket = client_socket
        self.sia = SentimentIntensityAnalyzer()
        self.action = {
            1: "Vote for Food Item",
            2: "Provide Feedback",
            3: "View Recommendations",
            4: "View Menu",
            5: "Update Profile",
            6: "view notifications",
            7: "Log Out"
        }
        self.menu_category = {
            1: "Breakfast",
            2: "Lunch",
            3: "Dinner"
        }
        self.details = employee_details

    def handle_employee_actions(self):
        while True:
            print(f"\nWelcome {self.details['name']}")
            for task in self.action:
                print(f"{task}. {self.action[task]}")
            choice = input("Enter choice: ")
            if choice == '1':
                isExit = False
                while not isExit:
                    isExit = self.viewRolledOutMenu()
                    if not isExit:
                        self.vote_for_food_item()
            elif choice == '2':
                emp_order = self.getMyTodayOrders()
                if emp_order <= 0:
                    print("Select the item id from the below menu.....")
                    self.view_menu()
                self.provide_feedback()
            elif choice == '3':
                self.view_recommendations()
            elif choice == '4':
                self.view_menu()
            elif choice == '5':
                self.update_profile()
            elif choice == '6':
                self.display_notifications()
            elif choice == '7':
                return 'logOut'
            else:
                print(f"Invalid choice, try again...")
                
    def update_profile(self):
        print("Please answer these questions to update your profile:")
        food_type = input("1) Please select one - Vegetarian, Non-Vegetarian, Eggetarian: ")
        spice_level = input("2) Please select your spice level - High, Medium, Low: ")
        preference = input("3) What do you prefer most? - North Indian, South Indian, Other: ")
        sweet_tooth = input("4) Do you have a sweet tooth? - Yes, No: ")

        profile_data = {
            'action': 'save_profile',
            'data': {
                'emp_id': self.details['user_id'],
                'food_type': food_type,
                'spice_level': spice_level,
                'preference': preference,
                'sweet_tooth': sweet_tooth
            }
        }
        self.client_socket.sendall(json.dumps(profile_data).encode())
        response = self.client_socket.recv(1024)
        response_data = json.loads(response.decode())
        print(response_data['message'])

    def vote_for_food_item(self):
        menu_id = int(input("Enter food ID to vote for: "))
        vote_request = {
            'action': 'vote_for_food_item',
            'data': {
                'item_id': menu_id,
                'emp_id': self.details['user_id']
                    }
        }
        self.client_socket.sendall(json.dumps(vote_request).encode())
        response = self.client_socket.recv(1024)
        response_data = json.loads(response.decode())
        print(response_data['message'])

    def view_menu(self):
        request = {'action': 'view_menu'}
        self.client_socket.sendall(json.dumps(request).encode())
        response = self.client_socket.recv(1024)
        response_data = json.loads(response.decode())
        menu = pd_df(data=response_data['menu'],columns=response_data['columns'])
        print(f"{response_data['message']}\n {menu.to_string(index=False)}")

    def viewRolledOutMenu(self):
        for category in self.menu_category:  
            print(f"{category}. {self.menu_category[category]}") 
        print(f"{len(self.menu_category)+1}. Back to action menu")
        menu_type = int(input("Enter your choice: "))
        if menu_type == len(self.menu_category)+1:
            return True
        request = {'action': 'display_RolledOutMenu', 'data':{'menu_type': self.menu_category[menu_type]}}
        self.client_socket.sendall(json.dumps(request).encode())
        response = self.client_socket.recv(1024)
        response_data = json.loads(response.decode())
        menu = pd_df(data=response_data['menu'],columns=response_data['columns'])
        print(f"{response_data['message']}\n {menu.to_string(index=False)}")
        
    def provide_feedback(self):
        item_id = int(input("Enter food item ID to provide feedback for: "))
        rate = float(input("How much you rate this item: "))
        while rate <0.0 or rate>6.0:
            rate = float(input("How much you rate this item: "))
        feedback = input("Enter your feedback: ")
        sentiment_score = self.sia.polarity_scores(feedback)['compound']
        feedback_request = {
            'action': 'provide_feedback',
            'data': {
                'item_id': item_id,
                'emp_id': self.details['user_id'], 
                'rating': rate,
                'feedback': feedback,
                'sentiment_score': sentiment_score}
            
        }
        self.client_socket.sendall(json.dumps(feedback_request).encode())
        response = self.client_socket.recv(1024)
        response_data = json.loads(response.decode())
        print(response_data['message'])
        
    def view_recommendations(self):
        for category in self.menu_category:  
            print(f"{category}. {self.menu_category[category]}") 
        menu_type = int(input("Please enter your menu category here: "))
        request = {'action': 'get_recommendation_employee',
                   'data' : {
                       'menu_type': self.menu_category[menu_type],
                       'emp_id':self.details['user_id']
                   }
        }
        self.client_socket.sendall(json.dumps(request).encode())
        response = self.client_socket.recv(1024)
        response_data = json.loads(response.decode())
        menu = pd_df(data=response_data['recommendation'],columns=response_data['column'])
        print(f"{response_data['message']}\n {menu.to_string(index=False)}")
        
    def getMyTodayOrders(self):
        request = {'action': 'my_todays_orders',
                   'data':  {
                       'emp_id': self.details['user_id'],
                   }
        }
        self.client_socket.sendall(json.dumps(request).encode())
        response = self.client_socket.recv(1024)
        response_data = json.loads(response.decode())
        if len(response_data['orders'])<=0:
            print(f"Dear {self.details['name']}, You haven't vote for today's menu")
        else:
            menu = pd_df(data=response_data['orders'],columns=response_data['columns'])
            print(f"Dear {self.details['name']}, {response_data['message']}\n {menu.to_string(index=False)}")
        return len(response_data['orders'])

    def display_notifications(self):
        notification_request = {
            'action': 'get_notifications',
            'data': {
                'emp_id': self.details['user_id']
            }
        }
        self.client_socket.sendall(json.dumps(notification_request).encode())
        response = self.client_socket.recv(1024)
        response_data = json.loads(response.decode())
        if len(response_data['notification'])>0:
            for notification in response_data['notification']:
                print(f"{notification[1]}:\n\t{notification[3]}")
                if notification[1].lower()=='feedback_required':
                    feedback = self.getFeedback(notification[1])
                    feedback['data']={'emp_id':notification[2],'item_name':notification[4]}
                    self.provideFeedback_discardItem(feedback)
        else:
            print("No new notification found.")
        
    def getFeedback(self, feedback_type):
        feedback = {}
        if feedback_type == 'feedback_required':
            questions = {
                1 : f"What didn’t you like?",
                2 : f"How would you like this to taste?",
                3 : "Share your mom’s recipe."
            }
            for ques_num in questions:
                feedback[ques_num] = input(f"\t{questions[ques_num]}\n\t")
                
        return feedback
    
    def provideFeedback_discardItem(self, feedback):
        reuest = {
            'action': 'provideFeedback_discardItem',
            'data': {
                'feedback': feedback,
                'emp_id': self.details['user_id']}
        }
        self.client_socket.sendall(json.dumps(reuest).encode())
        response = self.client_socket.recv(1024)
        response_data = json.loads(response.decode())
        print(response_data['message'])

