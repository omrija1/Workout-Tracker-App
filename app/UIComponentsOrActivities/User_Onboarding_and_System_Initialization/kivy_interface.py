# Import statements for Kivy framework
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from kivy.logger import Logger
# Import statements for other dependencies
from ...Database.User_Account_Data import db_setup  # Assuming this is the correct import path
import os
import sqlite3
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()


class BaseScreen(Screen):
    """
    Base class for different screens in the app.
    
    Attributes:
        layout (BoxLayout): A layout to contain widgets.
    
    Args:
        layout_orientation (str, optional): Orientation of the layout. Defaults to 'vertical'.
    """
    
    def __init__(self, layout_orientation: str = 'vertical', **kwargs):
        """
        Initialize the BaseScreen class.
        
        Args:
            layout_orientation (str): Orientation of the layout. 'vertical' or 'horizontal'.
            **kwargs: Additional keyword arguments.
        """
        super(BaseScreen, self).__init__(**kwargs)
        self.layout = BoxLayout(orientation=layout_orientation)
        self.add_widget(self.layout)
    
    def add_widget_to_layout(self, widget):
        """
        Add a widget to the existing layout.
        
        Args:
            widget (Widget): The Kivy widget to add..
        """
        self.layout.add_widget(widget)
class UserOnboarding(BaseScreen):
    """
    Screen for user onboarding.
    
    Methods:
        init_ui: Initialize the user interface.
        show_register_login: Switch to the register or login screen.
    """
    
    def __init__(self, **kwargs):
        """
        Initialize the UserOnboarding class.
        
        Args:
            **kwargs: Additional keyword arguments.
        """
        super(UserOnboarding, self).__init__(**kwargs)
        self.init_ui()

    def init_ui(self):
        """Initialize the UI elements for the user onboarding screen."""
        self.add_widget_to_layout(Label(text='Welcome!', size_hint_y=None, height=30, font_size=24))
        self.add_widget_to_layout(Button(text='Press to Continue', size_hint_y=None, height=50, on_press=self.show_register_login))
    
    def show_register_login(self, instance):
        """
        Handle the button press to switch to the register or login screen.
        
        Args:
            instance (Button): The button instance that triggered this method.
        """
        self.manager.manage_screens('register_login', 'add')
class RegisterLogin(BaseScreen):
    """
    Screen for choosing between registration and login.
    
    Methods:
        init_ui: Initialize the user interface.
        show_register_form: Switch to the registration screen.
        show_login_form: Switch to the login screen.
    """
    
    def __init__(self, **kwargs):
        """
        Initialize the RegisterLogin class.
        
        Args:
            **kwargs: Additional keyword arguments.
        """
        super(RegisterLogin, self).__init__(**kwargs)
        self.init_ui()

    def init_ui(self):
        """Initialize the UI elements for the register or login choice screen."""
        self.add_widget_to_layout(Label(text='Choose an Option:', size_hint_y=None, height=30, font_size=18))
        self.add_widget_to_layout(Button(text='Register', size_hint_y=None, height=50, on_press=self.show_register_form))
        self.add_widget_to_layout(Button(text='Login', size_hint_y=None, height=50, on_press=self.show_login_form))
        
    def show_register_form(self, instance):
        """
        Handle the button press to switch to the registration screen.
        
        Args:
            instance (Button): The button instance that triggered this method.
        """
        self.manager.manage_screens('register', 'add')

    def show_login_form(self, instance):
        """
        Handle the button press to switch to the login screen.
        
        Args:
            instance (Button): The button instance that triggered this method.
        """
        self.manager.manage_screens('login', 'add')
class RegisterScreen(BaseScreen):
    """
    Screen for user registration.
    
    Attributes:
        username (TextInput): Input field for username.
        email (TextInput): Input field for email.
        password (TextInput): Input field for password.
    
    Methods:
        init_ui: Initialize the user interface.
        create_text_input: Create a text input field.
        register_user: Handle the registration process.
        display_message: Display a message on the screen.
    """
    
    def __init__(self, **kwargs):
        """
        Initialize the RegisterScreen class.
        
        Args:
            **kwargs: Additional keyword arguments.
        """
        super(RegisterScreen, self).__init__(**kwargs)
        self.init_ui()

    def init_ui(self):
        """Initialize the UI elements for the registration screen."""
        self.username = self.create_text_input('Username')
        self.email = self.create_text_input('Email')
        self.password = self.create_text_input('Password', password=True)
        self.add_widget_to_layout(Button(text='Submit', size_hint_y=None, height=50, on_press=self.register_user))
        
    def create_text_input(self, hint_text: str, password: bool = False) -> TextInput:
        """
        Create and return a text input field.
        
        Args:
            hint_text (str): Placeholder text for the input field.
            password (bool): Whether this field should hide the text. Defaults to False.
            
        Returns:
            TextInput: The created text input field.
        """
        text_input = TextInput(hint_text=hint_text, password=password, size_hint_y=None, height=30)
        self.add_widget_to_layout(text_input)
        return text_input

    def register_user(self, instance):
        """
        Handle the registration process.
        
        Args:
            instance (Button): The button instance that triggered this method.
        """
        try:
            # Exception handling for database interactions
            result = db_setup.add_user(self.username.text, self.email.text, self.password.text)
            if result.get('is_successful'):
                self.manager.is_authenticated = True  # Set the flag to True
                self.manager.manage_screens('main_dashboard', 'add')
            else:
                self.display_message(result.get('message', 'An unknown error occurred.'))
        except Exception as e:
            self.display_message(f"An error occurred: {e}")

    def display_message(self, message: str):
        """
        Display a message on the screen and reinitialize the UI.
        
        Args:
            message (str): The message to display.
        """
        self.layout.clear_widgets()
        self.add_widget_to_layout(Label(text=message, size_hint_y=None, height=30, font_size=18))
        self.init_ui()
class LoginScreen(BaseScreen):
    """
    Screen for user login.
    
    Attributes:
        email (TextInput): Input field for email.
        password (TextInput): Input field for password.
    
    Methods:
        init_ui: Initialize the user interface.
        create_text_input: Create a text input field.
        login_user: Handle the login process.
        display_message: Display a message on the screen.
    """

    def __init__(self, **kwargs):
        """
        Initialize the LoginScreen class.
        
        Args:
            **kwargs: Additional keyword arguments.
        """
        super(LoginScreen, self).__init__(**kwargs)
        self.init_ui()

    def init_ui(self):
        """Initialize the UI elements for the login screen."""
        self.email = self.create_text_input('Email')
        self.password = self.create_text_input('Password', password=True)
        self.add_widget_to_layout(Button(text='Submit', size_hint_y=None, height=50, on_press=self.login_user))

    def create_text_input(self, hint_text: str, password: bool = False) -> TextInput:
        """
        Create and return a text input field.
        
        Args:
            hint_text (str): Placeholder text for the input field.
            password (bool): Whether this field should hide the text. Defaults to False.
            
        Returns:
            TextInput: The created text input field.
        """
        text_input = TextInput(hint_text=hint_text, password=password, size_hint_y=None, height=30)
        self.add_widget_to_layout(text_input)
        return text_input

    def login_user(self, instance):
        """
        Handle the login process.
        
        Args:
            instance (Button): The button instance that triggered this method.
        """
        try:
            # Assuming the database connection string is stored as an environment variable
            db_connection_string = os.environ.get('DB_CONNECTION_STRING', 'C:\\Workout-Tracker-App\\database.db')
            conn = sqlite3.connect(db_connection_string)
            result = db_setup.verify_login(self.email.text, self.password.text, conn)
            if result:
                self.manager.is_authenticated = True  # Set the flag to True
                self.manager.manage_screens('main_dashboard', 'add')
            else:
                self.display_message("Invalid email or password.")
        except Exception as e:
            self.display_message(f"An error occurred: {e}")

    def display_message(self, message: str):
        """
        Display a message on the screen and reinitialize the UI.
        
        Args:
            message (str): The message to display.
        """
        self.layout.clear_widgets()
        self.add_widget_to_layout(Label(text=message, size_hint_y=None, height=30, font_size=18))
        self.init_ui()
class MainDashboard(BaseScreen):
    """
    Screen for the main dashboard.
    
    Methods:
        init_ui: Initialize the user interface.
        navigate_to_screen: Navigate to a specified screen.
    """
    
    def __init__(self, **kwargs):
        """
        Initialize the MainDashboard class.
        
        Args:
            **kwargs: Additional keyword arguments.
        """
        super(MainDashboard, self).__init__(**kwargs)
        self.init_ui()

    def init_ui(self):
        """Initialize the UI elements for the main dashboard."""
        self.add_widget_to_layout(Label(text='Welcome to the Main Dashboard!', size_hint_y=None, height=30, font_size=24))
        self.add_widget_to_layout(Button(text='Go to Screen 1', size_hint_y=None, height=50, on_press=lambda instance: self.navigate_to_screen('screen_1')(instance)))
        self.add_widget_to_layout(Button(text='Go to Screen 2', size_hint_y=None, height=50, on_press=lambda instance: self.navigate_to_screen('screen_2')(instance)))


    def navigate_to_screen(self, screen_name):
        """
        Navigate to the specified screen.
        
        Args:
            screen_name (str): The name of the screen to navigate to.
        """
        def inner_function(instance):
            self.manager.manage_screens(screen_name, 'add')
        return inner_function

# New Screen1 and Screen2 classes
class Screen1(BaseScreen):
    def __init__(self, **kwargs):
        super(Screen1, self).__init__(**kwargs)
        self.add_widget_to_layout(Label(text='This is Screen 1', size_hint_y=None, height=30, font_size=24))

class Screen2(BaseScreen):
    def __init__(self, **kwargs):
        super(Screen2, self).__init__(**kwargs)
        self.add_widget_to_layout(Label(text='This is Screen 2', size_hint_y=None, height=30, font_size=24))

class Manager(ScreenManager):
    """
    Manager class to handle screen transitions.
    
    Methods:
        init_screens: Initialize the various screens.
    """
    
    def __init__(self, **kwargs):
        """
        Initialize the Manager class.
        
        Args:
            **kwargs: Additional keyword arguments.
        """
        super(Manager, self).__init__(**kwargs)
        self.screen_stack = []  # Stack to keep track of screen navigation
        self.is_authenticated = False  # Flag to check if the user is authenticated
        self.init_screens()

    def init_screens(self):
        """Initialize and add the different screens to the screen manager."""
        self.add_widget(UserOnboarding(name='onboarding'))
        self.add_widget(RegisterLogin(name='register_login'))
        self.add_widget(RegisterScreen(name='register'))
        self.add_widget(LoginScreen(name='login'))
        self.add_widget(MainDashboard(name='main_dashboard'))
        self.add_widget(Screen1(name='screen_1'))
        self.add_widget(Screen2(name='screen_2'))
        
    def manage_screens(self, screen_name, operation):
        if operation == 'add':
            self.screen_stack.append(screen_name)
        elif operation == 'remove' and self.screen_stack:
            self.screen_stack.pop()
        self.current = screen_name

    def go_back(self, window, key, *args):
        if key == 27:  # The escape key corresponds to the Android back button
            if self.screen_stack:
                self.screen_stack.pop()
                if self.screen_stack:
                    next_screen = self.screen_stack[-1]
                    if self.is_authenticated and next_screen in ['login', 'register']:
                        return True  # Block going back to login or register if authenticated
                    self.current = next_screen
                    self.screen_stack.pop()
                else:
                    self.current = 'main_dashboard'  # Navigate to main dashboard if stack is empty
                    self.screen_stack.append('main_dashboard')  # Add main dashboard to stack
            else:
                self.current = 'main_dashboard'  # Navigate to main dashboard if stack is empty
                self.screen_stack.append('main_dashboard')  # Add main dashboard to stack
            return True
        return False

class MyApp(App):
    """
    Main application class.
    
    Methods:
        build: Build and return the root widget.
    """
    
    def build(self):
        """
        Build and return the root widget for the application.
        
        Returns:
            Manager: The root widget.
        """
        # Initialize the database
        db_setup.initialize_database("database.db")
        sm = Manager()
        Window.bind(on_keyboard=sm.go_back) # bind back button
        sm.current = 'onboarding' # set the first screen
        sm.manage_screens('onboarding', 'add')
        return sm

# Main function to run the application
if __name__ == '__main__':
    """
    Entry point for the application. 
    Initializes and runs the Kivy app.
    """
    MyApp().run()
