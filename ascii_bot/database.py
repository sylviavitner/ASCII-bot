import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

class Database:
    def __init__(self):
        try:
            # Connect to db using env
            self.mydb = mysql.connector.connect(
                host=os.getenv("MYSQL_HOST"),
                user=os.getenv("MYSQL_USER"),
                password=os.getenv("MYSQL_PASSWORD"),
                database=os.getenv("MYSQL_DATABASE")
            )
            self.cursor = self.mydb.cursor() # set db cursor
            print("Connected to MySQL database.")
        except mysql.connector.Error as err:
            print(f"Error connecting to MySQL: {err}")
            exit()

    # Close database
    def __del__(self):
        if hasattr(self, 'mydb') and self.mydb.is_connected():
            self.mydb.close()
            print("MySQL connection closed.")

    # Check if a user is in the database
    def user_exists(self, discord_id):
        self.cursor.execute("SELECT 1 FROM users WHERE discord_id = %s", (discord_id,))
        return self.cursor.fetchone() is not None

    # Insert a new user into the db
    def insert_data(self, discord_id, discord_username, app_id):
        try:
            self.cursor.execute("INSERT INTO users (discord_id, discord_username, app_id) VALUES (%s, %s, %s)", (discord_id, discord_username, app_id))
            self.mydb.commit()
            return True
        except mysql.connector.Error as e:
            print(f"Error inserting data: {e}")
            self.mydb.rollback()
            return False

    # Get the user's app id from the db
    def get_app_id(self, discord_id):
        self.cursor.execute("SELECT app_id FROM users WHERE discord_id = %s", (discord_id,))
        result = self.cursor.fetchone()
        if result:
            return result[0]
        return None

    
