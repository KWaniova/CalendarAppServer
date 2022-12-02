
from dotenv import dotenv_values
from database import Database
import sqlite3
import uuid


config = dotenv_values(".env")


class DBSetup:

    def __init__(self):
        pass

    def db_init(self):
        print("Database creation")
        print(config.get("DB_NAME"))
        db = Database(config.get("DB_NAME"))
        sqlite3.register_converter('GUID', lambda b: uuid.UUID(bytes_le=b))
        db.cursor.execute(
            '''CREATE TABLE user (user_id GUID, first_name TEXT, last_name TEXT, e_mail TEXT, password TEXT, created_at DATETIME DEFAULT CURRENT_TIMESTAMP) ''')
        # self.create_users()

    def create_users(self):
        db = Database(config.get("DB_NAME"))
        db.insert_user("John", "Black",
                       "john@email.com", "John123")


if __name__ == "__main__":
    db = DBSetup()
    db.db_init()
