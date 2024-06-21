import nltk  
from users.recommendation_engine import Recommendation
from server.request_handler import RequestHandler
from server.db_operations import Database
from nltk.sentiment import SentimentIntensityAnalyzer
import pandas as pd

class Employee():
    def __init__(self,user):
        self.requestManger = RequestHandler()
        self.sia = SentimentIntensityAnalyzer()
        self.employee = user
        self.db = Database()
        self.tasks= {1: "Vote Item For Tomorrow",
                     2: "View Menu",
                     3: "Provide Feedback",
                     4: "Log Out"}
        
    def displayTasks(self):
        print(f"\nHello {self.employee['name']}... ")
        for task in self.tasks:  
            print(f"{task}. {self.tasks[task]}") 
        choice  = input("Please Enter your choice here: ")
        return choice
    
    def handleTasks(self,task):
        if task == '1':
            request = self.selectOrder()
        elif task == '2':
            request = self.viewMenu()
        elif task == '3':
            request = self.provideFeedback()
        elif task == '4':
            request = self.logout()
        return self.requestManger.manage_request(request)
        
    def selectOrder(self):
        menuType = {1 : "Breakfast",
                    2 : "Lunch",
                    3 : "Dinner"}
        
        for menu in menuType:
            print(f"{menu}. {menuType[menu]} ")
            
        request_data = {
            'client_type': 'employee',
            'action': 'vote_item',
            'category': menuType[int(input("Please select order type: "))],
            'emp_id': self.employee["user_id"]
        }
        return request_data
    
    def viewMenu(self):
        menuType = {1 : "Breakfast",
                    2 : "Lunch",
                    3 : "Dinner"}
        for menu in menuType:
            print(f"{menu}. {menuType[menu]} ")
        request_data =  {
            'client_type': 'employee',
            'action': 'view_menu',
            'menu_type': menuType[int(input("Please select order type: "))]
        }
        return self.requestManger.manage_request(request_data)
    
    def provideFeedback(self):
        item_id = self.getItemNeedToProvideFeedback()
        rating = int(input("Please give ratting to order(between 1 to 5): "))
        comment =  input("please provide your feedback comment: ")
        sentiment_score = self.sia.polarity_scores(comment)['compound']
        request_data = {
            'client_type': 'employee',
            'action': 'provide_feedback',
            'emp_id': self.employee["user_id"],
            'item_id': item_id,
            'rating': rating,
            'comment': comment,
            'sentiment_score': sentiment_score
        }
        return request_data
    
    def getItemNeedToProvideFeedback(self):
        request_data = {
            'client_type': 'employee',
            'action': 'my_vote',
            'emp_id': self.employee["user_id"]
        }
        myVote = self.requestManger.manage_request(request_data)
        print(pd.DataFrame(data = myVote,columns=["Item_id","Name"]).to_string(index=False))
        feedbackItem = int(input("Enter Item Id you want to provide feedback: "))
        return feedbackItem
                
    def _get_sentiment(self,item_id):
        total_sentiment = 0
        comment_count = 0
        query = "Select comment from feedback where item_id = %s"
        comments = self.db.execute_query(query,params=item_id)
        for comment in comments: 
            sentiment = self.sia.polarity_scores(comment)
            total_sentiment += sentiment['compound']
            comment_count += 1
        return total_sentiment / comment_count if comment_count > 0 else 0
    
    def get_order_recommendation(self):
        recommendation = Recommendation()
        rcmd_order = recommendation.recommend_to_employee(self.employee)
        return rcmd_order
        
    def _find_employee_previous_orders(self, employee_id):
        query = "select item_id,rating from feedbacks where emp_id = %s"
        emp_pastOrders = self.db.execute_query(query,params=employee_id)
        return emp_pastOrders
    
    def logout(self):
        request = {
            'client_type': 'login_logout',
            'action': 'logout',
            'user_id': self.employee["user_id"],
        }
        return request
    