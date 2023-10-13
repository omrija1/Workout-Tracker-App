import sqlite3
import os
import logging
from datetime import datetime

logging.basicConfig(filename='quote_manager.log', level=logging.DEBUG,
                        format='%(asctime)s - %(levelname)s - %(message)s')


class QuoteManager:
    """
    A manager to handle operations related to quotes within a SQLite database.
    
    Attributes:
        db_connection_string (str): The path to the SQLite database.
    """
    def __init__(self, database: str):
        """
        Initializes the QuoteManager with a connection string to the database.

        Args:
            database (str): The filename of the SQLite database.
        """
        # Define the database connection string, defaulting to a specific path if not set in environment variables
        self.db_connection_string = os.environ.get('DB_CONNECTION_STRING', f'C:\\Workout-Tracker-App\\{database}')

    def initialize_quotes_database(self, conn):
        """
        Initializes the database tables related to quotes and inserts sample quotes.

        Args:
            conn (sqlite3.Connection): The SQLite connection object.
        """
        # Creating the quotes and quote_display tables if they do not exist
        conn.execute('''
            CREATE TABLE IF NOT EXISTS quotes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                quote TEXT,
                author TEXT
            )
        ''')
        conn.execute('''
            CREATE TABLE IF NOT EXISTS quote_display (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                last_displayed DATE
            )
        ''')
        cursor = conn.cursor()
        # Check if the quotes table is empty and insert sample quotes if it is
        cursor.execute('SELECT COUNT(*) FROM quotes')
        if cursor.fetchone()[0] == 0:
            self.insert_sample_quotes(conn)
    
        # Check if the quote_display table is empty and insert an initial record if it is
        cursor.execute('SELECT COUNT(*) FROM quote_display')
        if cursor.fetchone()[0] == 0:
            conn.execute('INSERT INTO quote_display (last_displayed) VALUES (NULL)')

    def insert_sample_quotes(self, conn):
        """
        Inserts sample quotes into the quotes table.

        Args:
            conn (sqlite3.Connection): The SQLite connection object.
        """
        # Inserting predefined quotes into the quotes table
        conn.executemany('''
            INSERT INTO quotes (quote, author) VALUES (?, ?)
        ''', [
            ("The body is the servant of the mind; train both.", "Socrates"),
            ("Strength does not come from physical capacity, but from an indomitable will.", "Plato"),
            ("We are what we repeatedly do. Excellence, then, is not an act, but a habit.", "Aristotle"),
            ("Know thyself, know thy limits, break them.", "the Oracle of Delphi"),
            ("The pain you feel today will be the strength you feel tomorrow.", "GYMRATS"),
            ("If you still look good at the end of your workout, you didn’t train hard enough.", "GYMRATS"),
            ("For though the righteous fall seven times, they rise again.", "Proverbs 24:16 (NIV)")
        ])
        conn.commit()

    def get_last_displayed_date(self):
        """
        Retrieves the last displayed date of a quote from the quote_display table.
        Returns:
            datetime.date: The last displayed date, or None if no date is found.
        """
        conn = sqlite3.connect(self.db_connection_string)
        cursor = conn.cursor()
        # Retrieving the last displayed date from the quote_display table
        cursor.execute('SELECT last_displayed FROM quote_display WHERE id = 1')
        last_displayed = cursor.fetchone()
        conn.close()
        # Return the last displayed date if found, else return None
        return last_displayed[0] if last_displayed else None

    def update_last_displayed_date(self, date):
        """
        Updates the last displayed date of a quote in the quote_display table.
        Args:
        date (datetime.date): The date to be updated as the last displayed date.
        """
        try:
            with sqlite3.connect(self.db_connection_string) as conn:
                cursor = conn.cursor()
                cursor.execute('SELECT COUNT(*) FROM quote_display')
                if cursor.fetchone()[0] == 0:
                    conn.execute('INSERT INTO quote_display (last_displayed) VALUES (?)', (date,))
                else:
                    conn.execute('UPDATE quote_display SET last_displayed = ? WHERE id = 1', (date,))
        except sqlite3.Error as e:
            print(f"Database error: {e}")
        except Exception as e:
            print(f"Exception in _query: {e}")


    def get_todays_quote(self):
        """
        Retrieves today's quote. If the last displayed quote was shown today, it returns that quote.
        Otherwise, it selects a random quote, updates the last displayed date, and returns the selected quote.

        Returns:
        tuple: The quote and author in the format (quote, author), or (None, None) if not found.
        """
        try:
            conn = sqlite3.connect(self.db_connection_string)  # Establish a connection to the SQLite database.
            cursor = conn.cursor()  # Create a cursor object using the cursor() method.

        # Check if the last displayed date is today and return the same quote if so.
            cursor.execute('SELECT last_displayed FROM quote_display WHERE id = 1')
            last_displayed = cursor.fetchone()  # Fetch the result.
            print(f"Last displayed: {last_displayed}")  

            if last_displayed and last_displayed[0] == datetime.today().date():
                cursor.execute('SELECT quote, author FROM quotes WHERE id = (SELECT MAX(id) FROM quotes)')
            else:
                # If not, get a random quote and update the last displayed date to today.
                cursor.execute('SELECT quote, author FROM quotes ORDER BY RANDOM() LIMIT 1')
                cursor.execute('UPDATE quote_display SET last_displayed = ? WHERE id = 1', (datetime.today().date(),))
                conn.commit()  # Commit the transaction.

            result = cursor.fetchone()
            quote, author = result if result else (None, None)  # Retrieve the selected quote and author.
            conn.close()  # Close the database connection.
            print(f"Fetched quote: {quote}, author: {author}")
        # Return the selected quote and author, or None if not found.
        
            return quote, author
        except sqlite3.Error as e:
            logging.error(f"Database error: {e}")
            return None, None
        except Exception as e:
            logging.error(f"Exception: {e}")
            print(f"Error in get_todays_quote: {e}")
            return None, None
