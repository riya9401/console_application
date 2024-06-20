from server.db_operations import Database

class Recommendation:
    def __init__(self):
        self.db = Database()
        self.ratings_data = {}
        
    def recommend_to_employee(self,menu_type):
        query =  "SELECT item.item_id, item.name, fb.rating AS rating, item.category FROM food_item item LEFT JOIN feedback fb ON fb.item_id = item.item_id WHERE LOWER(item.availability) RLIKE '{}' OR LOWER(item.availability) = 'all' ORDER BY rating DESC;".format(menu_type.lower())
        recmd_request = self.db.execute_query(query)
        return recmd_request

    def recommend_to_chef(self,menuCategory=''):
        query = """SELECT item.item_id, item.name, fb.rating AS rating, item.category FROM food_item item LEFT JOIN feedback fb ON fb.item_id = item.item_id WHERE LOWER(item.availability) RLIKE '{}' OR LOWER(item.availability) = 'all' UNION SELECT item.item_id, item.name, fb.rating AS rating, item.category FROM food_item item RIGHT JOIN feedback fb ON fb.item_id = item.item_id WHERE LOWER(item.availability) RLIKE '{}' OR LOWER(item.availability) = 'all' ORDER BY rating DESC;""".format(menuCategory.lower(),menuCategory.lower())
        recmd_request = self.db.execute_query(query)
        return recmd_request
