from config.settings import *
from mysql.connector import errorcode,Error,connect

class Database:
    def __init__(self):
        self.conn = connect(
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
    
    def is_cursor_connected(self):
        try:
            self.cursor.execute("SELECT 1")
            return True
        except Error as e:
            print(f"Cursor is not connected: {e}")
            return False

    def close(self):
        self.cursor.close()
        self.conn.close()
        
    def open(self):
        self.conn._open_connection()
        self.cursor=self.conn.cursor()

