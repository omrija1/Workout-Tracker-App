import sqlite3
import hashlib
import re

def initialize_database():
    """
    Initialize the SQLite database and create the profiles table if it doesn't exist.
    """
    conn = sqlite3.connect('user_profiles.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS profiles
                 (username TEXT PRIMARY KEY,
                  email TEXT UNIQUE,
                  password TEXT)''')
    conn.commit()
    conn.close()

def validate_email_password(email, password):
    """
    Validate the email and password based on predefined rules.
    """
    email_valid = re.match(r"[^@]+@[^@]+\.[^@]+", email)
    password_strong = len(password) >= 8
    return email_valid and password_strong

def add_user(username, email, password):
    """
    Add a new user to the database.
    """
    if not validate_email_password(email, password):
        return "Invalid email format or weak password."
    conn = sqlite3.connect('user_profiles.db')
    c = conn.cursor()
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    try:
        c.execute("INSERT INTO profiles (username, email, password) VALUES (?, ?, ?)",
                  (username, email, hashed_password))
        conn.commit()
        return "User successfully registered."
    except sqlite3.IntegrityError:
        return "Username or email already exists."
    finally:
        conn.close()

def verify_login(email, password):
    """
    Verify if the login details are correct.
    """
    conn = sqlite3.connect('user_profiles.db')
    c = conn.cursor()
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    c.execute("SELECT * FROM profiles WHERE email=? AND password=?", (email, hashed_password))
    user = c.fetchone()
    conn.close()
    return bool(user)
