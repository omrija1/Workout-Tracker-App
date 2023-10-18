# Import required libraries for various functionalities
import os
import logging
import bcrypt
import sqlite3
import re
from dotenv import load_dotenv
from quote_manager import QuoteManager  # Import the QuoteManager class
from stats import Statistics_Manager


# Load environment variables from the .env file
load_dotenv()

# Configure logging settings
logging.basicConfig(filename='database_initialization.log', level=logging.DEBUG)


class DatabaseManager:
    def __init__(self, database: str):
        self.db_connection_string = os.environ.get('DB_CONNECTION_STRING', f'C:\\Workout-Tracker-App\\{database}')
    
    def initialize_database(self):
        try:
            logging.debug('Starting database initialization.')
            with sqlite3.connect(self.db_connection_string) as conn:
                logging.debug('Connecting to SQLite database.')
                self._create_profiles_table(conn)

                # Create stats manager instance and initialize stats table
                stats_manager = Statistics_Manager()
                stats_manager.initialize_statistics_database(conn)

                quote_manager = QuoteManager(self.db_connection_string)  # Initialize QuoteManager
                quote_manager.initialize_quotes_database(conn)  # Initialize quotes database
                self._set_pragmas(conn)
                conn.commit()
            logging.debug('Database initialization complete.')
        except sqlite3.Error as e:
            logging.error('Error initializing database: %s', str(e))
            raise
    
    def _create_profiles_table(self, conn):
        logging.debug('Creating profiles table if it does not exist.')
        conn.execute('''
            CREATE TABLE IF NOT EXISTS profiles (
                username TEXT PRIMARY KEY,
                email TEXT UNIQUE,
                password_hash TEXT
            )
        ''')

    def _set_pragmas(self, conn):
        logging.debug('Setting PRAGMAs.')
        conn.execute('PRAGMA secure_delete = ON')
        conn.execute('PRAGMA foreign_keys = ON')

class UserManager(DatabaseManager):
    def __init__(self, database: str):
        super().__init__(database)

    @staticmethod
    def validate_email_password(email: str, password: str) -> bool:
        logging.debug('Validating email and password.')
        email_valid = re.fullmatch(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', email)
        password_strong = len(password) >= 8
        return bool(email_valid and password_strong)

    def add_user(self, username: str, email: str, password: str) -> dict:
        logging.debug('Starting add_user function.')
        response = {'status': 'error', 'message': '', 'is_successful': False}
        reponse_stats = ""
        if len(username) > 12 or len(email) > 50:
            response['message'] = 'Username or email too long.'
            return response

        if not self.validate_email_password(email, password):
            response['message'] = 'Invalid email format or weak password.'
            return response

        try:
            with sqlite3.connect(self.db_connection_string) as conn:
                cursor = conn.cursor()
                cursor.execute('SELECT 1 FROM profiles WHERE username = ? OR email = ? LIMIT 1', (username, email))
                existing_user = cursor.fetchone()

                if existing_user:
                    response['message'] = 'Username or email already exists.'
                else:
                    salt = bcrypt.gensalt()
                    hashed_password = bcrypt.hashpw(password.encode(), salt).decode()
                    cursor.execute('INSERT INTO profiles (username, email, password_hash) VALUES (?, ?, ?)',
                                   (username, email, hashed_password))

                    conn.commit()
                    response['status'] = 'success'
                    response['message'] = 'User successfully registered.'
                    response['is_successful'] = True
        except Exception as e:
            logging.error(f'Error in add_user: {str(e)}')
            response['message'] = str(e)

        return response

    def add_stats_new_user(self, username: str) -> dict:
        """
        Creates entry into stats table for newly created user
        Args:
            username:

        Returns:
            Dictionary of response for stats entry
        """
        statistics_manager = Statistics_Manager()
        return statistics_manager.add_new_stats(username)

class AuthenticationManager(UserManager):
    def __init__(self, database: str):
        super().__init__(database)

    def verify_login(self, email: str, password: str, conn) -> bool:
        logging.debug('Starting verify_login function.')
        try:
            with conn:
                cursor = conn.cursor()
                cursor.execute('SELECT * FROM profiles WHERE email=?', (email,))
                user = cursor.fetchone()

                if user:
                    hashed_password = user[2]
                    logging.debug(f'Hashed Password from DB: {hashed_password}')
                    return bcrypt.checkpw(password.encode(), hashed_password.encode())
        except ValueError as e:
            logging.error(f'Invalid salt or hashed_password: {str(e)}')
            return False
        except Exception as e:
            logging.error(f'An error occurred in verify_login: {str(e)}')
            return False

        return False

# Initialize the database manager and perform the initial setup
if __name__ == '__main__':
    db_manager = DatabaseManager('database.db')
    db_manager.initialize_database()
