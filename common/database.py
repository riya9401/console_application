from config.config import Settings
import socket
import mysql.connector
from mysql.connector import errorcode

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

    def execute_query(self, query, params):
        self.cursor.execute(query, params)
        self.conn.commit()
