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
        """
            Initializes an instance of AuthenticationManagement and establishes a connection to the authentication database.
        """
        self.database_connection = None
        try:
            self.database_connection = sqlite3.connect(self.DATABASE_PATH)
        except sqlite3.Error as e:
            print(e)

    def __del__(self):
        """
            Closes the database connection when the instance of AuthenticationManagement is deleted.
        """
        if self.database_connection:
            self.database_connection.close()

    def create_user(self, email, password):
        """
            Creates a new user in the authentication database.

            Args:
                email (str): The email of the user.
                password (str): The user's password.

            Returns:
                None
        """
        cursor = self.database_connection.cursor()
        cursor.execute("INSERT INTO users (email, password) VALUES (?, ?)", (email, self.get_password_hash(password)))
        self.database_connection.commit()
        cursor.close()

    def check_user_exists(self, email):
        """
            Checks if a user with the given email already exists in the authentication database.

            Args:
                email (str): The email to check.

            Returns:
                bool: True if the user exists, False otherwise.
        """
        cursor = self.database_connection.cursor()
        cursor.execute("SELECT * FROM users WHERE email=?", (email,))
        user = cursor.fetchone()
        cursor.close()
        return user is not None

    def get_password_hash(self, password: str):
        """
            Hashes the provided password using the bcrypt hashing algorithm.

            Args:
                password (str): The password to hash.

            Returns:
                str: The hashed password.
        """
        return pwd_context.hash(password)

    def create_access_token(self, data: dict, expires_delta: Union[timedelta, None] = None):
        """
            Creates an access token using the provided data and expiration delta.

            Args:
                data (dict): The data to encode in the token.
                expires_delta (Union[timedelta, None]): The expiration delta for the token (default is 15 minutes).

            Returns:
                str: The encoded access token.
        """
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt

    def decode_token(self, token: str):
        """
            Decodes the provided JWT token.

            Args:
                token (str): The JWT token to decode.

            Returns:
                dict: The decoded data from the token.
        """
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

    def create_access_token_expires(self, email: str):
        """
            Creates an access token with a specified expiration time based on the configured expiration minutes.

            Args:
                email (str): The email associated with the token.

            Returns:
                str: The encoded access token with the specified expiration time.
        """
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        return self.create_access_token(data={"email": email}, expires_delta=access_token_expires)
