import uuid
import sqlite3
from sys import argv
from os import getenv
from dotenv import dotenv_values
import datetime


config = dotenv_values(".env")


class Database:

    def __init__(self, database_name):
        self.connection = sqlite3.connect(database_name)
        self.cursor = self.connection.cursor()

    def __del__(self):
        self.connection.close()

    def create_table(self, sql: str):
        self.cursor.execute(sql)
        self.connection.commit()

    def insert(self, table, *values):
        print(
            f"INSERT INTO {table} VALUES ({','.join('?' for _ in values)})", values)

        self.cursor.execute(
            f"INSERT INTO {table} VALUES ({','.join('?' for _ in values)})", values)
        self.connection.commit()

    def insert_user(self, first_name, last_name, e_mail, password):
        pass_hash = hash(password)
        id = uuid.uuid4()
        print(id)
        created_at = datetime.datetime.utcnow().isoformat()
        self.insert("user", id, first_name, last_name,
                    e_mail, pass_hash, created_at)


if len(argv) > 1 and argv[1] == 'setup':
    pass
    print("Database creation")
    print(config.get("DB_NAME"))
    db = Database(config.get("DB_NAME"))
    sqlite3.register_adapter(uuid.UUID, lambda u: u.bytes_le)
    sqlite3.register_converter('GUID', lambda b: uuid.UUID(bytes_le=b))
    db.cursor.execute(
        '''CREATE TABLE user (user_id GUID, first_name TEXT, last_name TEXT, e_mail TEXT, password TEXT, created_at DATETIME DEFAULT CURRENT_TIMESTAMP) ''')

if __name__ == "__main__":
    db = Database(config.get("DB_NAME"))
    db.insert_user("Samantha", "Black", "sam@email.com", "Samantha123")
