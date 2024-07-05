import json
from common.database import Database

class AdminRepository:
    def __init__(self):
        self.db = Database()
        self.table_name = 'food_item'
        self.feedback = 'feedback'
        self.notification = 'user_notification'
        self.itemDescription = 'item_description'
        self.scoring = 'item_score'
        
    def add(self, food_item_data):
        try:
            self._add_item(food_item_data)
            item_id = self._get_item_id(food_item_data)
            self._add_item_description(food_item_data, item_id)
            return {'status': 'success', 'message': 'Item added successfully', 'item_id': item_id}
        except Exception as e:
            return {'status': 'failure', 'message': str(e)}
    
    def _add_item(self, food_item_data):
        query = f"INSERT INTO {self.table_name} (name, price, availability, category) VALUES (%s, %s, %s, %s)"
        self.db.execute_query(query, params=(food_item_data['name'], food_item_data['price'], food_item_data['availability'], food_item_data['category']))
        
    def _get_item_id(self, food_item_data):
        query = f"SELECT item_id FROM {self.table_name} WHERE name = %s AND price = %s AND availability= %s AND category=%s"
        result = self.db.execute_query(query, params=(food_item_data['name'], food_item_data['price'], food_item_data['availability'], food_item_data['category']))
        return result[0][0]
    
    def _add_item_description(self, description, item_id):
        query = f"INSERT INTO {self.itemDescription} (item_id, foodType, spiceLevel, prefrenceType) VALUES (%s, %s, %s, %s)"
        self.db.execute_query(query, params=(item_id, description['food_type'], description['spice_level'], description['preference']))

    def update(self, food_item_data):
        try:
            update_type = food_item_data['updating_field'].lower()
            if update_type in ["item name", "price", "availability", "category"]:
                response = self._update_item_info(food_item_data)
            elif update_type in ["food type", "spice level", "preference"]:
                response = self._update_item_description(food_item_data)
            return response
        except Exception as e:
            return {'status': 'failure', 'message': str(e)}
    
    def _update_item_info(self, food_item_data):
        column = self._get_column_name(food_item_data['updating_field'])
        item_name = self._get_item_name(food_item_data['id'])
        query = f"UPDATE {self.table_name} SET {column} = %s WHERE item_id = %s"
        self.db.execute_query(query, params=(food_item_data['updating_value'], food_item_data['id']))
        message = f"{item_name}'s {column} is updated to {food_item_data['updating_value']}."
        return {'status': 'success', 'message': message, 'item_id': food_item_data['id']}
    
    def _update_item_description(self, new_description):
        column = self._get_column_name(new_description['updating_field'])
        item_name = self._get_item_name(new_description['id'])
        query = f"UPDATE {self.itemDescription} SET {column} = %s WHERE item_id = %s"
        self.db.execute_query(query, params=(new_description['updating_value'], new_description['id']))
        message = f"{item_name}'s {column} is updated to {new_description['updating_value']}."
        return {'status': 'success', 'message': message, 'item_id': new_description['id']}
    
    def _get_column_name(self, field_name):
        mapping = {
            "Item Name": "name",
            "Price": "price",
            "Availability": "availability",
            "Category": "category",
            "Food Type": "foodType",
            "Spice Level": "spiceLevel",
            "Preference": "prefrenceType"
        }
        return mapping[field_name]

    def _get_item_name(self, item_id):
        query = f"SELECT name FROM {self.table_name} WHERE item_id = %s"
        result = self.db.execute_query(query, params=(item_id,))
        return result[0][0]
    
    def remove(self, food_item_data):
        try:
            item_name = self._get_item_name(food_item_data['id'])
            query = f"DELETE FROM {self.table_name} WHERE item_id = %s"
            self.db.execute_query(query, params=(food_item_data['id'],))
            message = f"{item_name} is removed from cafeteria."
            return {'status': 'success', 'message': message, 'item_id': food_item_data['id']}
        except Exception as e:
            return {'status': 'failure', 'message': str(e)}
    
    def view_all_items(self):
        try:
            query = f"SELECT item_id,name,cast(price as char) as price,availability,category FROM {self.table_name}"
            menu = self.db.execute_query(query)
            message = "Cafeteria Menu:"
            columns = ["item_id", "name", "price", "availability", "category"]
            return {'status': 'success', 'message': message, 'menu': menu, "columns": columns}
        except Exception as e:
            return {'status': 'failure', 'message': str(e)}
    
    def get_discard_list(self):
        try:
            query = query = f"""
            SELECT item.name, CAST(item_sc.average_rating AS CHAR) as avg_rating, CAST(item_sc.average_sentiment AS CHAR) as avg_sentiment_score
            FROM {self.table_name} item
            JOIN {self.scoring} item_sc ON item.item_id = item_sc.item_id
            JOIN {self.feedback} fb ON item.item_id = fb.item_id
            WHERE item_sc.average_rating < 2 
                OR LOWER(fb.comment) LIKE '%tasteless%' 
                OR LOWER(fb.comment) LIKE '%extremely bad experience%' 
                OR LOWER(fb.comment) LIKE '%very poor%' 
                OR LOWER(fb.comment) LIKE '%worst%'
            ORDER BY avg_rating DESC, avg_sentiment_score ASC;
        """

            discard_items = self.db.execute_query(query)
            return {'status': 'success', 'discard_list': discard_items}
        except Exception as e:
            return {'status': 'failure', 'message': str(e)}
    
    def remove_item_by_name(self, item_name):
        try:
            item_id = self.db.execute_query(query=f'SELECT item_id FROM {self.table_name} WHERE name = %s', params=(item_name,))
            if item_id:
                return self.remove({'id': item_id[0][0]})
            return {'status': 'error', 'message': 'Item not found'}
        except Exception as e:
            return {'status': 'failure', 'message': str(e)}
    
    def request_feedback(self, item_name):
        try:
            message = f"We are trying to improve your experience with {item_name}. Please provide your feedback and help us.\n"
            employees = self._get_all_employee_ids()
            for employee_id in employees:
                query = f"INSERT INTO {self.notification} (notify_type, user_id, notification, item_name) VALUES ('feedback_required', %s, %s, %s)"
                self.db.execute_query(query, params=(employee_id, message, item_name))
            return {'status': 'success'}
        except Exception as e:
            return {'status': 'failure', 'message': str(e)}
    
    def _get_all_employee_ids(self):
        query = "SELECT user_id FROM user_access WHERE LOWER(user_role)='employee'"
        result = self.db.execute_query(query)
        return [row[0] for row in result]

    def send_notification(self, notification_type, data):
        try:
            message, response_message, recipients = self._get_notification_details(notification_type, data)
            receivers = self._get_recipients_ids(recipients)
            for user_id in receivers:
                query = f"INSERT INTO {self.notification} (notify_type, user_id, notification, item_name) VALUES (%s, %s, %s, %s)"
                self.db.execute_query(query, params=(notification_type, user_id, message, data['name']))
            return {'status': 'success', 'message': response_message}
        except KeyError as e:
            if 'name' in str(e):
                try:
                    data['name'] = self._get_item_name(data['id'])
                    return self.send_notification(notification_type, data)
                except Exception as retry_e:
                    return {'status': 'failure', 'message': str(retry_e)}
            return {'status': 'failure', 'message': str(e)}
        except Exception as e:
            return {'status': 'failure', 'message': str(e)}
    
    def _get_notification_details(self, notification_type, data):
        if notification_type == "newItemAdded":
            message = f"{data['name']} added to cafeteria Menu"
            response_message = "Notification sent for newly added item"
            recipients = ('employee', 'chef')
        elif notification_type == "itemUpdated":
            message = f"{data['name']} is now updated with {data['updating_field']} as {data['updating_value']}"
            response_message = "Notification sent for updated item"
            recipients = ("employee",)
        elif notification_type == "itemRemoved":
            message = f"{data['name']} is now removed from cafeteria"
            response_message = "Notification sent for removed item"
            recipients = ('employee', 'chef')
        return message, response_message, recipients
    
    def _get_recipients_ids(self, recipients):
        query = f"SELECT user_id FROM user_access WHERE LOWER(user_role) IN {recipients}"
        result = self.db.execute_query(query)
        return [row[0] for row in result]
