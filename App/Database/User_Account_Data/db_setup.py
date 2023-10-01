import os
import bcrypt
import sqlite3
import hashlib
import re
import logging

def initialize_database(database_name):
    """
    Initialize the SQLite database and create the profiles table if it doesn't exist.
    """
    try:
        with sqlite3.connect(database_name) as conn:
            c = conn.cursor()
            c.execute('''CREATE TABLE IF NOT EXISTS profiles
                     (username TEXT PRIMARY KEY,
                      email TEXT UNIQUE,
                      password_hash TEXT)''')
            c.execute("PRAGMA secure_delete = ON")
            c.execute("PRAGMA foreign_keys = ON")
            conn.commit()
    except sqlite3.Error as e:
        logging.error("Error initializing database: %s", str(e))
        
    
    
# Function to validate_email_password
def validate_email_password(email, password):
    """
    Validate the email and password based on predefined rules.
    """
    email_valid = re.fullmatch(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", email)
    if email_valid is None:
        return False
    
    password_strong = len(password) >= 8
    return email_valid and password_strong

# Function to add_user
def add_user(username, email, password):
    response = {'status': 'error', 'message': '', 'is_successful': False}
    if len(username) > 12 or len(email) > 50:
        response['message'] = "Username or email too long."
        return response
    
    if not validate_email_password(email, password):
        response['message'] = "Invalid email format or weak password."
        return response
    
    try:
        db_connection_string = os.environ.get('DB_CONNECTION_STRING')
        if db_connection_string:
            with sqlite3.connect(db_connection_string) as conn:
                c = conn.cursor()
                
                c.execute("SELECT 1 FROM profiles WHERE username = ? OR email = ? LIMIT 1", (username, email))
                existing_user = c.fetchone()
                
                if existing_user:
                    response['message'] = "Username or email already exists."
                else:
                    salt = bcrypt.gensalt()
                    hashed_password = bcrypt.hashpw(password.encode(), salt).decode()
                    c.execute("INSERT INTO profiles (username, email, password) VALUES (?, ?, ?)",
                              (username, email, hashed_password))
                    conn.commit()
                    response['status'] = 'success'
                    response['message'] = "User successfully registered."
                    response['is_successful'] = True
        else:
            response['message'] = "DB_CONNECTION_STRING environment variable is not set."
    except Exception as e:
        response['message'] = str(e)
        
    return response

# Function to verify_login
def verify_login(email, password, conn):
    """
    Verify if the login details are correct.
    """
    with conn:
        c = conn.cursor()
        c.execute("SELECT * FROM profiles WHERE email=?", (email,))
        user = c.fetchone()
        if user:
            hashed_password = user[1]
            if bcrypt.checkpw(password.encode(), hashed_password.encode()):
                return True
    return False
