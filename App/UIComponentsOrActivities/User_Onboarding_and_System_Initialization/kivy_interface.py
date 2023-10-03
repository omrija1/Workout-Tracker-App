# # Import required libraries for SQLite database and Kivy interface
import sqlite3
import os
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.app import App
# # Import necessary Kivy modules for building the UI components
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from ...Database.User_Account_Data import db_setup

# # UserOnboarding Class: Manages the user onboarding process in the app


# Kivy Interface
# # __init__: Constructor to initialize the UserOnboarding class and its widgets
# UserOnboarding Class
class UserOnboarding(BoxLayout):
    
    def __init__(self, **kwargs):
        super(UserOnboarding, self).__init__(**kwargs)
# # show_register_login: Clears existing widgets and shows Register/Login options
        self.orientation = 'vertical'
        self.add_widget(Label(text='Welcome!', size_hint_y=None, height=30, font_size=24))
        self.add_widget(Button(text='Press to Continue', size_hint_y=None, height=50, on_press=self.show_register_login))
        
        # Function to show_register_login
    def show_register_login(self, instance):
        self.clear_widgets()
# # show_register_form: Clears existing widgets and shows the user registration form
        self.add_widget(Label(text='Choose an Option:', size_hint_y=None, height=30, font_size=18))
        self.add_widget(Button(text='Register', size_hint_y=None, height=50, on_press=self.show_register_form))
        self.add_widget(Button(text='Login', size_hint_y=None, height=50, on_press=self.show_login_form))
        
        # Function to show_register_form
    def show_register_form(self, instance):
        self.clear_widgets()
        self.username = TextInput(hint_text='Username', size_hint_y=None, height=30)
        self.email = TextInput(hint_text='Email', size_hint_y=None, height=30)
# # register_user: Handles the registration of a new user using the details from the form
        self.password = TextInput(hint_text='Password', password=True, size_hint_y=None, height=30)
        self.add_widget(self.username)
        self.add_widget(self.email)
        self.add_widget(self.password)
        self.add_widget(Button(text='Submit', size_hint_y=None, height=50, on_press=self.register_user))
        
        # Function to register_user
# # show_login_form: Clears existing widgets and shows the user login form
    def register_user(self, instance):
        result = db_setup.add_user(self.username.text, self.email.text, self.password.text)
        self.clear_widgets()
        self.add_widget(Label(text=str(result.get('message', result)), size_hint_y=None, height=30, font_size=18))


        
        # Function to show_login_form
# # login_user: Handles the login process using the details from the form
    def show_login_form(self, instance):
        self.clear_widgets()
        self.email = TextInput(hint_text='Email', size_hint_y=None, height=30)
        self.password = TextInput(hint_text='Password', password=True, size_hint_y=None, height=30)
        self.add_widget(self.email)
        self.add_widget(self.password)
        self.add_widget(Button(text='Submit', size_hint_y=None, height=50, on_press=self.login_user))
        
# # MyApp Class: The main application class
# Function to login_user
    def login_user(self, instance):
        db_connection_string = os.environ.get('DB_CONNECTION_STRING', 'C:\\Workout-Tracker-App\\database.db')
# # build: Builds the application interface using Kivy
        conn = sqlite3.connect(db_connection_string)
        if db_setup.verify_login(self.email.text, self.password.text, conn):
            self.clear_widgets()
            self.add_widget(Label(text="Login successful.", size_hint_y=None, height=30, font_size=18))
        else:
# # Entry point: The main function that runs the Kivy application
            self.clear_widgets()
            self.add_widget(Label(text="Invalid email or password.", size_hint_y=None, height=30, font_size=18))

# MyApp Class
class MyApp(App):

    def build(self):
        sm = MyScreenManager()
        sm.add_widget(UserOnboardingScreen(name='onboarding'))
        return sm
    
# Function to build
        db_setup.initialize_database("database.db")
        return UserOnboarding()


if __name__ == '__main__':
    MyApp().run()

class UserOnboardingScreen(Screen):
    pass

class MyScreenManager(ScreenManager):
    pass
