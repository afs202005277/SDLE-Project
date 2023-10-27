import os
import sqlite3
from jose import jwt
from passlib.context import CryptContext
from datetime import timedelta, datetime
from typing import Union
import env

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
ACCESS_TOKEN_EXPIRE_MINUTES = env.ACCESS_TOKEN_EXPIRE_MINUTES
SECRET_KEY = env.SECRET_KEY
ALGORITHM = env.ALGORITHM
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

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
        cursor.execute("INSERT INTO users (email, password) VALUES (?, ?)", (email, self.get_password_hash(password)))
        self.database_connection.commit()
        cursor.close()
    
    def check_user_exists(self, email):
        cursor = self.database_connection.cursor()
        cursor.execute("SELECT * FROM users WHERE email=?", (email,))
        user = cursor.fetchone()
        cursor.close()
        return user is not None


    def get_password_hash(self, password: str):
        return pwd_context.hash(password)

    def create_access_token(self, data: dict, expires_delta: Union[timedelta, None] = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt


    def decode_token(self, token: str):
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    
    def create_access_token_expires(self, email: str):
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        return self.create_access_token(data={"email": email}, expires_delta=access_token_expires)