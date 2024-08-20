from config.configuration import Settings
import socket
from mysql.connector import errorcode,Error,connect
import mysql.connector
class Database:
    def __init__(self):
        setting=Settings()
        self.conn = mysql.connector.connect(
            host=setting.HOST,
            user=setting.USER,
            password=setting.PASSWORD,
            database=setting.DATABASE
        )
        self.cursor = self.conn.cursor()

    def execute_query(self, query, params=None):
        self.cursor.execute(query, params)
        if query.strip().upper().startswith("SELECT"):
            return self.cursor.fetchall()
        else:
            self.conn.commit()
            
