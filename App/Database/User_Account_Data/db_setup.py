# # Import required libraries for various functionalities such as OS, encryption, database, and logging
import os
import bcrypt
import sqlite3
import hashlib
import re
import logging

# # Configure basic logging settings for database initialization

logging.basicConfig(filename='database_initialization.log', level=logging.DEBUG)
# # Function to initialize the SQLite database
def initialize_database(database: str) -> None:
    try:
# # Log the beginning of the database initialization process
        logging.debug('Starting database initialization.')
        
# # Retrieve or set the default database connection string
        db_connection_string = os.environ.get('DB_CONNECTION_STRING', 'C:\\Workout-Tracker-App\\' + database)
        
        # Connect to the SQLite database
        logging.debug('Connecting to SQLite database.')
# # Connect to the SQLite database
        with sqlite3.connect(db_connection_string) as conn:
            
            # Create the profiles table if it doesn't exist
# # Create the 'profiles' table if it doesn't already exist
            logging.debug('Creating profiles table if it does not exist.')
            conn.execute('''
                CREATE TABLE IF NOT EXISTS profiles (
                    username TEXT PRIMARY KEY,
                    email TEXT UNIQUE,
                    password_hash TEXT
                )
            ''')
            
# # Enable SQLite PRAGMAs for secure delete and foreign key constraints
            # Enable secure delete and foreign key constraints
            logging.debug('Setting PRAGMAs.')
            conn.execute("PRAGMA secure_delete = ON")
            conn.execute("PRAGMA foreign_keys = ON")
# # Commit changes to the SQLite database
            
            # Commit the changes to the database
            logging.debug('Committing changes to the database.')
# # Log the completion of database initialization
            conn.commit()
        
        logging.debug('Database initialization complete.')
# # Log and handle any SQLite errors during initialization
        
    except sqlite3.Error as e:
        logging.error("Error initializing database: %s", str(e))
    
    
# # Function to validate email and password based on predefined rules
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
# # Validate email format using regex


logging.basicConfig(filename='add_user.log', level=logging.DEBUG)
# # Validate password length (must be at least 8 characters)
os.environ['DB_CONNECTION_STRING'] = 'C:\\Workout-Tracker-App\\database.db'


# Function to add user
# # Configure logging settings for adding a user
def add_user(username, email, password):
    db_connection_string = os.environ.get('DB_CONNECTION_STRING', 'C:\\Workout-Tracker-App\\database.db')
    logging.debug('Starting add_user function.')
# # Function to add a new user to the 'profiles' table in the database
    response = {'status': 'error', 'message': '', 'is_successful': False}
    if len(username) > 12 or len(email) > 50:
        response['message'] = "Username or email too long."
        return response
    
    if not validate_email_password(email, password):
# # Function to verify login credentials against the database
        response['message'] = "Invalid email format or weak password."
        return response
    
    try:
        logging.debug(f'Using DB connection string: {db_connection_string}')
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
                    c.execute("INSERT INTO profiles (username, email, password_hash) VALUES (?, ?, ?)",
                              (username, email, hashed_password))
                    conn.commit()
                    response['status'] = 'success'
                    response['message'] = "User successfully registered."
                    response['is_successful'] = True
        else:
            response['message'] = "DB_CONNECTION_STRING environment variable is not set."
    except Exception as e:
        logging.error(f'Error in add_user: {str(e)}')
        response['message'] = str(e)
        
    return response



logging.basicConfig(filename='verify_login.log', level=logging.DEBUG)
# Function to verify_login
def verify_login(email, password, conn):
    """
    Verify if the login details are correct.
    """
    try:
        with conn:
            c = conn.cursor()
            c.execute("SELECT * FROM profiles WHERE email=?", (email,))
            user = c.fetchone()

            if user:
                hashed_password = user[2]  
                
                # Log the hashed_password for debugging
                logging.debug(f"Hashed Password from DB: {hashed_password}")

                # Check password
                if bcrypt.checkpw(password.encode(), hashed_password.encode()):
                    return True
    except ValueError as e:
        logging.error(f"Invalid salt or hashed_password: {str(e)}")
        return False
    except Exception as e:
        logging.error(f"An error occurred in verify_login: {str(e)}")
        return False

    return False


