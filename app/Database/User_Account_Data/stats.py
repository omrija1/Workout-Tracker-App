import sqlite3
import os
import logging

logging.basicConfig(filename="statistic.log",
                    level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s'
                    )


class Statistics_Manager():
    """
    A manager to handle the operations to stats for each user's profile within a SQLite database

    Attributes:
        db_connection_string (str): The path to the SQLite database.
    """

    def __init__(self):
        """
        Inititalizes the Statistics Manager with a connection string to the database.


        """

        # Define the database connection string, defaulting to a specific path if not set in environment variables
        self.db_connection_string = os.environ.get('DB_CONNECTION_STRING', r'C:\Workout-Tracker-App\{database}')


    def initialize_statistics_database(self, conn):
        """
        Initialize the database table related to statistics
        Args:
            conn: (sqlite3.Connection): The SQLite connection object.


        """
        logging.debug('Creating stats table if it does not exist.')
        # Creating the quotes and quote_display tables if they do not exist
        conn.execute('''
                   CREATE TABLE IF NOT EXISTS stats (
                       id INTEGER PRIMARY KEY AUTOINCREMENT,
                       age INTEGER,
                       height TEXT,
                       gender TEXT,
                       weight INTEGER,
                       goal_weight INTEGER,
                       last_updated DATE,
                       username TEXT
                       
                   )
               ''')

        #cursor = conn.cursor()

    def add_new_stats(self, username):
        """
        Insert into stats table entry for newly created user: username

        Args:
            conn, username:

        """
        logging.debug('Starting add_new_stats functionnnn.')
        response = {'status': 'error', 'message': '', 'is_successful': False}

        try:
            with sqlite3.connect(self.db_connection_string) as conn:
                cursor = conn.cursor()
                cursor.execute('SELECT 1 FROM profiles WHERE (username) = (?)', (username,))
                existing_user = cursor.fetchone()

                if existing_user:
                    # response['message'] = 'Username or email already exists.'
                    cursor.execute('INSERT INTO stats (username) VALUES (?)', (username,))
                    conn.commit()
                    response['status'] = 'success'
                    response['message'] = f'User stats entry successfully generated for user: {username}.'
                    response['is_successful'] = True
                else:
                    response['message'] = f'user: {username} does not exist in database'

        except Exception as e:
            logging.error(f'Error in add_stats_new_user: {e}')
            response['message'] = str(e)

        return response
    def set_last_updated_date(self):
        """
        Sets the displayed date of the last time the profile was updated


        """
        try:
            pass
        except sqlite3.Error as e:
            logging.error(f"Database error: {e}")
            return None
        except Exception as e:
            logging.error(f"Exception: {e}")
            return None



