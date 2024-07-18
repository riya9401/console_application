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
            6: "View Notifications",
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
            try:
                if choice == '1':
                    self.handle_vote_for_food()
                elif choice == '2':
                    self.handle_provide_feedback()
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
            except Exception as e:
                print(f"An error occurred: {str(e)}")

    def handle_vote_for_food(self):
        isExit = False
        while True:
            isExit = self.view_rolled_out_menu()
            if isExit:
                break
            elif isExit is not None:
                self.vote_for_food_item()
            print()
            

    def handle_provide_feedback(self):
        emp_order = self.get_my_today_orders()
        if emp_order < 1:
            print("Ups, You haven't voted for today.\n")
            print("Please enter the item id from the below menu that you ordered manually.....")
            self.view_menu()
        self.provide_feedback()

    def update_profile(self):
        try:
            profile_data = self.collect_profile_data()
            self.send_request('save_profile', profile_data)
        except Exception as e:
            print(f"Failed to update profile: {str(e)}")

    def collect_profile_data(self):
        print("Please answer these questions to update your profile:")
        food_type = input("1) Please select one - Vegetarian, Non-Vegetarian, Eggetarian: ")
        spice_level = input("2) Please select your spice level - High, Medium, Low: ")
        preference = input("3) What do you prefer most? - North Indian, South Indian, Other: ")
        sweet_tooth = input("4) Do you have a sweet tooth? - Yes, No: ")
        return {
            'emp_id': self.details['user_id'],
            'food_type': food_type,
            'spice_level': spice_level,
            'preference': preference,
            'sweet_tooth': sweet_tooth
        }

    def vote_for_food_item(self):
        try:
            menu_id = int(input("Enter food ID to vote for: "))
            self.send_request('vote_for_food_item', {'item_id': menu_id, 'emp_id': self.details['user_id']})
        except Exception as e:
            print(f"Failed to vote for food item: {str(e)}")

    def view_menu(self):
        try:
            self.send_request('view_menu', {})
        except Exception as e:
            print(f"Failed to view menu: {str(e)}")

    def view_rolled_out_menu(self):
        for category in self.menu_category:
            print(f"{category}. {self.menu_category[category]}")
        print(f"{len(self.menu_category)+1}. Back to action menu")
        menu_type = int(input("Enter your choice: "))
        if menu_type == len(self.menu_category)+1:
            return True
        try:
            return self.send_request('display_RolledOutMenu', {'menu_type': self.menu_category[menu_type]})
        except Exception as e:
            print(f"Failed to view rolled-out menu for:  {self.menu_category[menu_type]}")
            return True

    def provide_feedback(self):
        try:
            item_id, rate, feedback, sentiment_score = self.collect_feedback_data()
            feedback_data = {
                'item_id': item_id,
                'emp_id': self.details['user_id'],
                'rating': rate,
                'feedback': feedback,
                'sentiment_score': sentiment_score
            }
            self.send_request('provide_feedback', feedback_data)
        except Exception as e:
            print(f"Failed to provide feedback: {str(e)}")

    def collect_feedback_data(self):
        item_id = int(input("Enter food item ID to provide feedback for: "))
        rate = float(input("How much you rate this item: "))
        while rate < 0.0 or rate > 6.0:
            rate = float(input("How much you rate this item: "))
        feedback = input("Enter your feedback: ")
        sentiment_score = self.sia.polarity_scores(feedback)['compound']
        return item_id, rate, feedback, sentiment_score

    def view_recommendations(self):
        try:
            for category in self.menu_category:
                print(f"{category}. {self.menu_category[category]}")
            menu_type = int(input("Please enter your menu category here: "))
            self.send_request('get_recommendation_employee', {'menu_type': self.menu_category[menu_type], 'emp_id': self.details['user_id']})
        except Exception as e:
            print(f"Failed to view recommendations: {str(e)}")

    def get_my_today_orders(self):
        try:
            return self.send_request('my_todays_orders', {'emp_id': self.details['user_id']})
        except Exception as e:
            print(f"Failed to get today's orders: {str(e)}")
            return 0

    def display_notifications(self):
        try:
            self.send_request('get_notifications', {'emp_id': self.details['user_id']})
        except Exception as e:
            print(f"Failed to display notifications: {str(e)}")

    def send_request(self, action, data):
        request = {'action': action, 'data': data}
        self.client_socket.sendall(json.dumps(request).encode())
        response_data = self.get_response()
        print(response_data['message'])
        if action == 'view_menu' or action == 'display_RolledOutMenu' or action == 'get_recommendation_employee':
            if len(response_data['menu'])>0:
                menu = pd_df(data=response_data['menu'], columns=response_data['columns'])
                print(f"{menu.to_string(index=False)}")
            else:
                if action == 'view_menu':
                    print(f"Menu not for {data['menu_type']} category.")
                elif action == 'display_RolledOutMenu':
                    print(f"Menu is not rolled out for tomorrow's {data['menu_type']} menu.")
                elif action == 'get_recommendation_employee':
                    print(f"Recommendation not found for {data['menu_type']}")
                return
        elif action == 'my_todays_orders':
            if len(response_data['todays_orders']) > 0:
                menu = pd_df(data=response_data['todays_orders'], columns=response_data['columns'])
                print(f"Dear {self.details['name']}, {response_data['message']}\n {menu.to_string(index=False)}")
            return len(response_data['todays_orders'])
        elif action == 'get_notifications':
            self.handle_notifications(response_data['notifications'])
        return False

    def handle_notifications(self, notifications):
        if len(notifications) > 0:
            for notification in notifications:
                print(f"\n{notification[1]}:\n{notification[3]}")
                if notification[1].lower() == 'feedback_required':
                    if input("Would you like to provide feedback(yes/no): ").lower() in ["yes","y"]:
                        feedback = self.get_feedback('feedback_required')
                        feedback['data'] = {'emp_id': notification[2], 'item_name': notification[4]}
                        self.provide_feedback_discard_item(feedback)
                self.clear_notification(notification[0])
        else:
            print("No new notification found.")

    def get_feedback(self, feedback_type):
        feedback = {}
        if feedback_type == 'feedback_required':
            questions = {
                1: "What didn’t you like?",
                2: "How would you like this to taste?",
                3: "Share your mom’s recipe."
            }
            for ques_num in questions:
                feedback[f'{ques_num}'] = input(f"{questions[ques_num]}\n")
        return feedback

    def provide_feedback_discard_item(self, feedback):
        try:
            feedback['emp_id'] = self.details['user_id']
            self.send_request('provideFeedback_discardItem', feedback)
        except Exception as e:
            print(f"Failed to provide feedback for discarded item: {str(e)}")
            
    def clear_notification(self,notification_id):
        try:
            self.send_request('clear_notification', notification_id)
        except Exception as e:
            print(f"Failed to clear notification where notification id is {notification_id} due to: {str(e)}")

    def get_response(self):
        response = b''
        try:
            response_size = json.loads(self.client_socket.recv(1024).decode())
            while response_size:
                chunk = self.client_socket.recv(1024)
                if not chunk:
                    break
                response += chunk
                response_size -= len(chunk)
            response_data = json.loads(response.decode())
            return response_data
        except Exception as e:
            print(f"Failed to get response: {str(e)}")
            return {}
