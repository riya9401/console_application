import mysql.connector
from config.settings import *

class Database:
    def __init__(self):
        self.conn = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        self.cursor = self.conn.cursor()

    def execute_query(self, query, params=None):
        self.cursor.execute(query, params)
        if self.cursor.with_rows:
            result = self.cursor.fetchall()
        else:
            result = None
        self.conn.commit()
        return result

    def close(self):
        self.cursor.close()
        self.conn.close()
