class Recommendation:
    def __init__(self, db_connection):
        self.db_connection = db_connection
        self.ratings_data = {}
        self._load_ratings_data()

    def _load_ratings_data(self):
        query = "SELECT rating from recomendation_item"
        self.ratings_data = self.db.execute_query(query)
        
    def recommend_to_employee(self, emp_prev_data):
        pastOrders = self._find_employee_previous_orders(employee_id)
        max_score = 0
        rcmd_item = None
        item_scores = {}
        
        for order in emp_prev_data:
            for itemCount in range(0,len(order)):
                item = order[itemCount][0]
                rating = [order[itemCount][1],]
                if item_scores[item]:
                    item_scores[item] = item_scores[item].append(rating)
                else:
                    item_scores[item] = rating
                    
        for item in item_scores:
            score = item_scores[item][0]
            if len(item_scores[item]) > 1:
                for score_index in range(0,len(item_scores[item])):
                    score = score + item_scores[item][score_index]
            item_scores[item] = score

        for item in item_scores:
            score = item_scores[item]
            if score < max_score:
                max_score = score
                rcmd_item = item

        return rcmd_item

    def recommend_to_chef(self,defaultCount=5):
        query = "SELECT * FROM recommendation ORDER BY average_rating DESC"
        highRatingItems = self.db.execute_query(query)
        
        rcmd_items = {}
        for itemCount in range(defaultCount):
            item = highRatingItems[itemCount][1]
            rating = highRatingItems[itemCount][2]
            rcmd_items[item] = rating
        return rcmd_items

    

    

    