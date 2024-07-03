from common.database import Database
import json

class AdminRepository:
    def __init__(self):
        self.db = Database()
        self.table_name = 'food_item'
        self.feedback = 'feedback'
        self.notification = 'user_notification'
        self.itemDescription = 'item_description'
        self.scoring = 'item_score'
        
    def add(self, food_item_data):
        addItem = "insert into {} (name,price,availability,category) values(%s,{},%s,%s)".format(self.table_name,food_item_data['price'])
        self.db.execute_query(addItem, params=(food_item_data['name'],food_item_data['availability'],food_item_data['category']))
        
        getItemID = "select item_id from {} where name = %s and price = {} and availability= %s and category=%s".format(self.table_name,food_item_data['price'])
        itemID = self.db.execute_query(getItemID, params=(food_item_data['name'],food_item_data['availability'],food_item_data['category']))
        description = self.addItemDescription(food_item_data,itemID[0][0])
        return {'status': 'success', 'message': 'item added successfully', 'item_id': itemID[0][0]}
    
    def addItemDescription(self, description,itemId):
        addItemDesc = "insert into {} (item_id,foodType,spiceLevel,prefrenceType) values (%s,%s,%s,%s)".format(self.itemDescription)
        return self.db.execute_query(addItemDesc, params=(itemId,description['food_type'],description['spice_level'],description['preference']))

    def update(self, food_item_data):
        update_type = food_item_data['updating_field'].lower()
        if update_type in ["item name","price","availability","category"]:
            self.updateItemInfo(food_item_data)
        elif update_type in ["food type", "spice level", "preference"]:
            self.updateItemDescription(food_item_data)
    
    def updateItemInfo(self,food_item_data):
        update_type = food_item_data['updating_field']
        if update_type == "Item Name":
            column = "name"
        elif update_type == "Price":
            column = "price"
        elif update_type == "Availability":
            column = "availability"
        elif update_type == "Category":
            column  = "category"
        itemName = self.db.execute_query(query='select name from {} where item_id = {}'.format(self.table_name,food_item_data['id']))
        updateItem = 'UPDATE {} SET `{}` = %s WHERE item_id = %s'.format(self.table_name,column)
        self.db.execute_query(updateItem,params=(food_item_data['updating_value'],int(food_item_data['id'])))
        message = f"{itemName[0][0]}'s {column} is updated to {food_item_data['updating_value']}."
        return {'status': 'success', 'message': message, 'item_id': food_item_data['id']}
    
    def updateItemDescription(self,newDescription):
        update_type = newDescription['updating_field'].lower()
        if update_type == "food type":
            column = "foodType"
        elif update_type == "spice level":
            column = "spiceLevel"
        elif update_type == "preference type":
            column = "prefrenceType"
        itemName = self.db.execute_query(query='select name from {} where item_id = {}'.format(self.table_name,newDescription['id']))
        updateItem = 'UPDATE {} SET `{}` = %s WHERE item_id = %s'.format(self.itemDescription,column)
        self.db.execute_query(updateItem,params=(newDescription['updating_value'],int(newDescription['id'])))
        message = f"{itemName[0][0]}'s {column} is updated to {newDescription['updating_value']}."
        return {'status': 'success', 'message': message, 'item_id': newDescription['id']}
    
    def remove(self, food_item_data):
        itemName = self.db.execute_query(query='select name from {} where item_id = {}'.format(self.table_name,food_item_data['id']))
        deleteItem = "DELETE FROM {} where item_id = %s".format(self.table_name,)
        self.db.execute_query(deleteItem,params=(food_item_data['id'],))
        message = f"{itemName[0][0]} is removed from cafeteria."
        return {'status': 'success', 'message': message, 'item_id': food_item_data['id']}
    
    def view_all_items(self):
        getMenu  = "SELECT * FROM {}".format(self.table_name)
        menu = self.db.execute_query(getMenu)
        message = "Cafeteria Menu:"
        coulumns = ["item_id","name","price","availability","category"]
        return {'status': 'success', 'message': message, 'menu': menu, "columns": coulumns}
    
    def get_discard_list(self):
        getDiscardItems = f"""
        SELECT item.name, cast(item_sc.average_rating as char) as avg_rating, cast(item_sc.average_sentiment as char) as avg_sentiment_score
        FROM {self.table_name} item
        JOIN {self.scoring} item_sc ON item.item_id = item_sc.item_id
        join {self.feedback} fb ON item.item_id = fb.item_id
        where item_sc.avg_rating < 2 OR lower(fb.comment) LIKE '%tasteless%' OR lower(fb.comment) LIKE '%extremely bad experience%' OR lower(fb.comment) LIKE '%very poor%' OR lower(fb.comment) LIKE '%worst%';
        """
        discardItems = self.db.execute_query(getDiscardItems)
        return {'status': 'success', 'discard_list': discardItems}
    
    def remove_item_by_name(self, item_name):
        itemID = self.db.execute_query(query='select item_id from {} where name = %s'.format(self.table_name), params=(item_name,))
        if itemID:
            return self.remove({'id': itemID[0][0]})
        return {'status': 'error', 'message': 'Item not found'}
    
    def request_feedback(self, item_name):
        message = f"We are trying to improve your experience with {item_name}. Please provide your feedback and help us.\n"
        employee =self.getAllEmployeesIds()
        for employee_id in range(len(employee)):
            insertFb  ="insert into {} (notify_type,user_id,notification,item_name) values ('feedback_required',%s,%s,%s);".format(self.notification) 
            self.db.execute_query(insertFb,params=(employee[employee_id][0],message,item_name))
        return {'status': 'success'}
    
    def getAllEmployeesIds(self):
        getEmpId = "select user_id from user_access where lower(user_role)='employee';"
        return self.db.execute_query(getEmpId)

    def sendNotification(self, notification_type,data):
        try:
            if notification_type == "newItemAdded":
                message = f"{data['name']} added to cafeteria Menu"
                response_message = "notification send for newly added item"
                recipents = ('employee','chef')
            elif notification_type == "itemupdated":
                message = f"{data['name']} is now update with {data['updating_field']} as {data['updating_value']}"
                response_message = "notification send for update item"
                recipents = ("employee",)
            elif notification_type == "itemRemoved":
                message = f"{data['name']} is now removed from cafeteria"
                response_message = "notification send for update item"
                recipents = ('employee','chef')
                
            reciever =self.db.execute_query(query="select user_id from user_access where lower(user_role) in {};".format(recipents))
            for user in range(len(reciever)):
                pushNotification  ="insert into {} (notify_type,user_id,notification,item_name) values (%s,%s,%s,%s);".format(self.notification) 
                self.db.execute_query(pushNotification,params=(notification_type,reciever[user][0],message,data['name']))
            return {'status': 'success','message':response_message}
        except KeyError as e:
            if 'name' in str(e):
                try:
                    data['name'] = self.db.execute_query("select item_name from {} where item_id=%s;".format(self.table_name), params=(data['id'],))[0][0]
                    return self.send_notification(notification_type, data)
                except Exception as retry_e:
                    return {'status': 'failure', 'message': str(retry_e)}
            else:
                return {'status': 'failure', 'message': str(e)}
        except Exception as e:
            return {'status': 'failure', 'message': str(e)}
                
            