import json
import os
import sqlite3

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

class AuthenticationManagement:
    DATABASE_PATH = f"{ROOT_DIR}/../databases/authentication/authentication.db"

    def __init__(self):
        self.database_connection = None
        try:
            self.database_connection = sqlite3.connect(self.DATABASE_PATH)
        except sqlite3.Error as e:
            print(e)
    
    def __del__(self):
        if self.database_connection:
            self.database_connection.close()
    
    def create_user(self, email, password):
        cursor = self.database_connection.cursor()
        cursor.execute("INSERT INTO users (email, password) VALUES (?, ?)", (email, password))
        self.database_connection.commit()
        cursor.close()
    
    def get_user(self, email):
        cursor = self.database_connection.cursor()
        cursor.execute("SELECT * FROM users WHERE email=?", (email,))
        user = cursor.fetchone()
        cursor.close()
        return user
    
    def get_user_by_id(self, user_id):
        cursor = self.database_connection.cursor()
        cursor.execute("SELECT * FROM users WHERE id=?", (user_id,))
        user = cursor.fetchone()
        cursor.close()
        return user
    
    def get_user_by_token(self, token):
        cursor = self.database_connection.cursor()
        cursor.execute("SELECT * FROM users WHERE token=?", (token,))
        user = cursor.fetchone()
        cursor.close()
        return user
    
    def check_user_exists(self, email, password):
        cursor = self.database_connection.cursor()
        cursor.execute("SELECT * FROM users WHERE email=? AND password=?", (email, password,))
        user = cursor.fetchone()
        cursor.close()
        return user is not None
    
    def verify_user_token(self, token):
        self.update_tokens()
        cursor = self.database_connection.cursor()
        cursor.execute("SELECT * FROM authentication_tokens WHERE token=?", (token,))
        user = cursor.fetchone()
        cursor.close()
        return user is not None
    
    def update_tokens(self):
        cursor = self.database_connection.cursor()
        cursor.execute("INSERT INTO authentication_tokens (token, user_id, expiration_date) VALUES (?, ?, ?)", ("token", 1, "2021-01-01 00:00:00"))
        self.database_connection.commit()
        cursor.execute("DELETE FROM authentication_tokens (token, user_id, expiration_date) WHERE token=?", ("token",))
        self.database_connection.commit()
        cursor.close()
    
    def create_token(self, user_id, token, expiration_date):
        cursor = self.database_connection.cursor()
        cursor.execute("INSERT INTO authentication_tokens (token, user_id, expiration_date) VALUES (?, ?, ?)", (token, user_id, expiration_date))
        self.database_connection.commit()
        cursor.close()