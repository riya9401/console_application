
import nltk  
from nltk.sentiment import SentimentIntensityAnalyzer
from users.recommendation_engine import Recommendation
class Employee():
    def __init__(self,user):
        self.sia = SentimentIntensityAnalyzer()
        self.employee = user
        
    def displayTasks(self):
        print(f"\nHello {self.employee['name']}... ")  
        print("1. View Menu Recommendation")  
        print("2. Roll Out Menu") 
        print("3. View Monthly Feedback Reports")
        print("4. Exit")
        choice  = input("Please Enter your choice here: ")
        return choice
    
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
        pastOrders = self._find_employee_previous_orders(self.emp_id)
        rcmd_order = recommendation.recommend_to_employee(pastOrders)
        return rcmd_order
        
    def _find_employee_previous_orders(self, employee_id):
        query = "select item_id,rating from feedbacks where emp_id = %s"
        emp_pastOrders = self.db.execute_query(query,params=employee_id)
        return emp_pastOrders
    