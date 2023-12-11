import os
import sqlite3
import re
import uuid
import json
import logging
import bcrypt
from sqlalchemy import text
from sqlalchemy.orm import sessionmaker
from app.Database.models import Profile, Stats, Library, Quotes, Quote_Display,engine


# logging
logging.basicConfig(filename='database_initialization_alch.log',
                    level=logging.DEBUG)
logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

quotes_url = "quotes.json"
# session = Session()
# tmp_user1 = Profile(username="apple", email="apple@gmail.com", password="apple11!")
# tmp_user2 = Profile(username="apple", email="banana@gmail.com", password="apple11!")
# tmp_user3 = Profile(username="chowder", email="chowder@gmail.com", password="apple11!")


quote_d = Quote_Display(quote="Don't Leave Me Kuta", author="Kubera")

quotes_flag = 1
# Session = sessionmaker(bind=engine)


class DatabaseManager:

    def __init__(self):
        Session = sessionmaker(bind=engine)
        self.session = Session()
        # self.add_user("apple", "apple@gmail.com", "apple")
        pass



    def add_temp_quotes(self):
        # Grab data from quotes json file
        with open(quotes_url) as quote_conn:
            # Load quotes into dict quoates_data
            if quotes_flag:
                quotes_data = json.load(quote_conn)

            quote_list = [Quotes(quote=x["quote"], author=x["author"]) for x in quotes_data["quotes"]]


        # Add temp quotes to quotes db
        self.session.add_all(quote_list)
        quote_list = self.session.query(Quotes).all()
        self.session.commit()

        # Print list of temp quotes
        # [x.display_quote() for x in quote_list]




    def init_db(self):
        # create db
        try:
            logging.debug('Database initialization starting...')
            create_db()
            logging.debug('Database initialization complete...')
            self.add_temp_quotes()
            user_manager = UserManager()
            user_manager.add_temp_profile()

        except sqlite3.Error as e:
            logging.error('Error initializing database: %s', str(e))


    # Add Quotes

class UserManager:

    def __init__(self):
        self.Session = sessionmaker(bind=engine)

    def validate_email_password(self, new_user) -> bool:
        logging.debug('Validating email and password.')
        email_valid = re.fullmatch(
            r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', new_user.email)
        password_strong = len(new_user.password) >= 8
        return bool(email_valid and password_strong)

    def add_user(self, username:str, email:str, password:str):

        new_user = Profile(username, email, password)
        logging.debug("...Starting Function..    add_user")

        # response object
        response = {'status': 'error', 'message': '', 'is_successful': False}

        # check length of username or email
        if len(new_user.username) > 12 or len(new_user.email) > 50:
            response['message'] = 'Username or email too long.'
            return response

        # check validation of email and password
        if not self.validate_email_password(new_user):
            response['message'] = 'Invalid email format or weak password.'
            return response

        try:
            with self.Session() as session, session.begin() :

                user_exists = session.query(Profile).filter_by(username=new_user.username).one_or_none()

                # if user exist set error message
                if user_exists:
                    response['message'] = 'Username or email already exists.'
                    print(f"Error: {response['message']}")
                    return response
                # if user doesn't exist add to database
                else:

                    # created hashed password
                    salt = bcrypt.gensalt()

                    # assign hashed password to new_user object
                    new_user.password = bcrypt.hashpw(
                        new_user.password.encode(), salt).decode()

                    # user added to database
                    session.add(new_user)

                    # query newly added user to gain user_id for assicated stats table
                    user_exists = session.query(Profile).filter_by(username=new_user.username).one_or_none()
                    # session.commit()

                    # create stats object
                    logging.debug("Creating stats object..")
                    new_stat = Stats(id=user_exists.id)
                    logging.debug("Adding stats object to database...")

                    session.add(new_stat)
                    logging.debug("Stats object successfully added to db")
                    new_stat = session.query(Stats).filter_by(id=user_exists.id).one_or_none()
                    # session.commit()

                    response['status'] = 'success'
                    response['message'] = 'User successfully registered.'
                    response['is_successful'] = True
                    return response


        except Exception as e:
            logging.error(f'Error in add_user: {e}')
            response['message'] = str(e)

            session.rollback()
        logging.debug(f"Exiting Function..    add_user\n-----------------------------------------")


    def add_temp_profile(self):
        user1 = Profile(username="apple", password="apple", email="apple@gmail.com")
        tmp_user1 = Profile(username="apple", email="apple@gmail.com", password="apple11!")
        tmp_user2 = Profile(username="banana", email="banana@gmail.com", password="apple11!")
        tmp_user3 = Profile(username="chowder", email="chowder@gmail.com", password="apple11!")

        user_list = []
        user_list.append(user1)
        user_list.append(tmp_user1)
        user_list.append(tmp_user2)
        user_list.append(tmp_user3)

        for x in user_list:
            self.add_user(x.username, x.email, x.password)



# todo: convert authentication manager
class AuthenticationManager:

    # Init function.   Initializes session
    def __init__(self):
        self.Session = sessionmaker(bind=engine)


    # verify login
    def verify_login(self, new_email: str, password: str) -> Profile:
        logging.debug('Starting verify_login function...')
        try:
            with self.Session() as session, session.begin():

                # check database for existing email
                is_existing_email = session.query(Profile).filter_by(email=new_email.lower()).one_or_none()

                # if a matching email is found in database check the hashed password
                if is_existing_email:
                    hashed_password = is_existing_email.password
                    logging.debug(
                        f'Hashed Password from DB: {hashed_password}')

                    # check if passwords match return user to manager object
                    if bcrypt.checkpw(password.encode(), hashed_password.encode()):
                        return is_existing_email.id
                        print(f"Current user: {is_existing_email.id}")
                    # return
        except ValueError as e:
            logging.error(f'Invalid salt or hashed_password: {str(e)}')
            return False
        except Exception as e:
            logging.error(f'An error occurred in verify_login: {str(e)}')
            return False

        return False


# db_manager = DatabaseManager()
# db_manager.init_db()

# user = Profile("apple","apple@gamil.com","apple")

# am_manager = AuthenticationManager()
# print(f"Status of Login: {am_manager.verify_login('Apple@gmail.com','apple11!')}")

# if __name__ == "__main__":
print("Should run")
db_manager = DatabaseManager()
db_manager.init_db()