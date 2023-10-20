# Import statements for Kivy framework
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.popup import Popup
from kivy.core.window import Window
from kivy.logger import Logger
from kivy.lang.builder import Builder
from kivy.properties import ObjectProperty
# Import statements for other dependencies
from app.database.db_setup import DatabaseManager, UserManager, AuthenticationManager
import os
import sqlite3
from dotenv import load_dotenv
from app.lib.quote_manager import QuoteManager
from datetime import datetime


Logger.debug('This is a debug message')


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
    
    def init_ui(self):
        """
        Initialize the UI elements for the screen.
        This method should be overridden by derived screen classes.
        """
        Logger.warning("BaseScreen: init_ui method not overridden in derived class")
    
    def displayPop(self, pop_title,pop_label_text):
        """
        Displays a popup to the active screen

        Args:
            pop_title: Title for Popup window
            pop_label_text: Text for Label inside Popup window

        """

        # Create Popup
        pop = Popup(title=pop_title,
                    content=Label(text=pop_label_text),
                    size_hint=(None,None), size=(400, 400))

        # Display Popup window to screen
        pop.open()

    def display_message(self, message: str):
        """
        Display a message on the screen and reinitialize the UI.
        
        Args:
            message (str): The message to display.
        """
        self.layout.clear_widgets()
        self.layout.add_widget(Label(text=message, size_hint_y=None, height=30, font_size=18))
        self.init_ui()
        
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
        self.layout.add_widget(text_input)
        return text_input


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
        self.layout.add_widget(Label(text='Welcome!', size_hint_y=None, height=30, font_size=24))
        self.layout.add_widget(Button(text='Achieve Harmony. Push Your Limits!', size_hint_y=None, height=50, on_press=self.show_register_login))
    
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
        self.layout.add_widget(Label(text='Choose an Option:', size_hint_y=None, height=30, font_size=18))
        self.layout.add_widget(Button(text='Register', size_hint_y=None, height=50, on_press=self.show_register_form))
        self.layout.add_widget(Button(text='Login', size_hint_y=None, height=50, on_press=self.show_login_form))
        
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
        self.layout.add_widget(Button(text='Submit', size_hint_y=None, height=50, on_press=self.register_user))
        

    def register_user(self, instance):
        """
        Handle the registration process.
        
        Args:
            instance (Button): The button instance that triggered this method.
        """
        try:
            # Exception handling for database interactions
            user_manager = UserManager('database.db')  # Initialize UserManager
            result = user_manager.add_user(self.username.text, self.email.text, self.password.text)  # Use add_user method
            result_stats = user_manager.add_stats_new_user(self.username.text)

            if result.get('is_successful') and result_stats.get('is_successful'):

                self.manager.is_authenticated = True  # Set the flag to True
                self.manager.manage_screens('main_dashboard', 'add')
            else:
                self.display_message(result.get('message', 'An unknown error occurred.'))
        except Exception as e:
            self.display_message(f"An error occurred: {e}")


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
        self.layout.add_widget(Button(text='Submit', size_hint_y=None, height=50, on_press=self.login_user))

    def login_user(self, instance):
        """
        Handle the login process.
        
        Args:
            instance (Button): The button instance that triggered this method.
        """
        try:
            auth_manager = AuthenticationManager('database.db')  # Initialize AuthenticationManager
            db_connection_string = os.environ.get('DB_CONNECTION_STRING', 'C:\\Workout-Tracker-App\\database.db')
            conn = sqlite3.connect(db_connection_string)
            result = auth_manager.verify_login(self.email.text, self.password.text, conn)  # Use verify_login method
            if result:

                self.manager.is_authenticated = True  # Set the flag to True
                self.manager.manage_screens('main_dashboard', 'add')
                self.displayPop(pop_title="Login Successful", pop_label_text='Welcome to the Arena of Self-Mastery')
            else:
                self.display_message("Invalid email or password.")
                self.displayPop(pop_title="Login Failed",pop_label_text="Incorrect email or password")
        except Exception as e:
            self.display_message(f"An error occurred: {e}")


class MainDashboard(BaseScreen):
    """
    Screen for the main dashboard.
    
    Methods:
        init_ui: Initialize the user interface.
        navigate_to_screen: Navigate to a specified screen.
        fetch_and_display_quote: Fetch today's quote and display it.
    """
    
    def __init__(self, manager_instance,**kwargs):
        """
        Initialize the MainDashboard class.
        
        Args:
            **kwargs: Additional keyword arguments.
        """
        super(MainDashboard, self).__init__(**kwargs)
        self.quote_manager = QuoteManager('database.db')
        self.manager_instance = manager_instance
        self.fetch_and_display_quote()

    def fetch_and_display_quote(self):
        """
        Fetch and display today's quote, adhering to logic in get_todays_quote.
        Initialize the UI afterward with the retrieved quote text.
        """
        try:
            today = datetime.today().date()  # Get today's date
            last_displayed_date = self.quote_manager.get_last_displayed_date()
            last_displayed_date_obj = (
                datetime.strptime(last_displayed_date, "%Y-%m-%d").date()
                if last_displayed_date else None
            )

            if last_displayed_date_obj is None or last_displayed_date_obj < today:
                quote, author = self.quote_manager.get_todays_quote()
                quote_text = (
                    f'"{quote}" - {author}' if quote and author else 'No quote found.'
                )
                # Update the last displayed date
                self.quote_manager.update_last_displayed_date(today) 
            else:
                quote, author = self.quote_manager.get_todays_quote()
                quote_text = (
                    f'"{quote}" - {author}' if quote and author else 'No last quote found.'
                )
            # Initialize the UI with the fetched or last displayed quote
            self.init_ui(quote_text)
        except Exception as e:
            Logger.error(f"Error fetching quote: {e}")
            self.init_ui("Error fetching quote.")

    def init_ui(self, quote_text):
        """
        Initialize the UI elements for the main dashboard.
        
        Args:
            quote_text (str): The quote text to be displayed on the dashboard.
        """
        self.layout.add_widget(Label(text=quote_text, size_hint_y=None, height=30, font_size=24))
        self.layout.add_widget(Button(text='Go to Screen 1', size_hint_y=None, height=50, on_press=self.manager_instance.navigate_to_screen('screen_1')))
        self.layout.add_widget(Button(text='Go to Settings', size_hint_y=None, height=50, on_press=self.manager_instance.navigate_to_screen('settings')))


# New Screen1 and Screen2 classes
class SettingsScreen(BaseScreen):
    # May not need this
    settings_name = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(SettingsScreen, self).__init__(**kwargs)


class ProfileScreen(BaseScreen):
    """
       Class to handle most of the functionality of the Profile Screen

       Methods:
           initialize_anchor_buttons: Init text for the two buttons at bottom of the screen
           initialize_slider: initialize label for weight slider and set max value for slider
           initialize_grid_layout: initialize label/textput pair for each setting in profile_options[]
           add_grid_labels: create and return standardized  label for the gridlayout
           add_grid_textinput: create and return standardized textinput for gridlayout

    """
    anchor_name = ObjectProperty(None)          # Anchor Layout id
    box_name = ObjectProperty(None)             # Inner Box Layout id
    grid_name = ObjectProperty(None)            # Grid Layout id
    return_button = ObjectProperty(None)        # Return Button id
    update_button = ObjectProperty(None)        # Update Button id
    slider = ObjectProperty(None)               # slider object
    label_slider = ObjectProperty(None)         # label for slider


    # todo add user name or image to profile

    def __init__(self, **kwargs):
        super(ProfileScreen,self).__init__(**kwargs)
        self.profile_widgets = {}
        self.profile_options = ["weight goal", "age", "gender", "height"]       # array of profile settings
        self.initialize_anchor_buttons()
        self.initialize_grid_layout()
        self.initialize_slider()
        self.init_base_functionality_to_widgets()


    def init_base_functionality_to_widgets(self):

        # currently only applies to text input widgets

        # weight goal
        self.profile_widgets["weight goal"]["widget_right"].on_text_validate = self.on_change_weightgoal

        # height goal
        self.profile_widgets["height"]["widget_right"].on_text_validate = self.on_change_height

        # age goal
        self.profile_widgets["age"]["widget_right"].on_text_validate = self.on_change_age

        # gender
        self.profile_widgets["gender"]["widget_right"].on_text_validate = self.on_change_gender

        # weight sider
        # self.profile_widgets["slider"]["widget_right"].on_text_validate = self.on_change_slider()

    def initialize_anchor_buttons(self):
        """ Function to intialize functionality for bottom buttons of profile screen"""
        self.return_button.text = "Go to Settings"
        self.update_button.text = "Update Profile"

    def initialize_slider(self):
        """Initialize label text for slider"""
        self.label_slider.text = f"Current Weight: {self.slider.value}"
        self.slider.max= 500

        # add widget to self.profile_widgets
        self.profile_widgets["slider"] = {'widget_left':self.label_slider,
                                          'widget_right':self.slider,
                                          'value': self.slider.value}

        # logging to verify widgets stores properly
        Logger.debug(f"slider\n----")
        Logger.debug(f"Left Widget: {self.profile_widgets['slider']['widget_left']}")
        Logger.debug(f"Right Widget: {self.profile_widgets['slider']['widget_right']}\n----")
        Logger.debug(f"Obj Properties Slider: {self.slider.max_value}")

    def initialize_grid_layout(self):
        """add a label/textinput pair for each profile setting in profile_options to layout"""

        for x in self.profile_options:

            g_label = self.add_grid_Labels(x)
            g_text = self.add_grid_textinput()

            # add widgets to screen layout
            self.grid_name.add_widget(g_label)
            self.grid_name.add_widget(g_text)

            # add widgets for x in self.profile_widgets
            self.profile_widgets[x] = {"widget_left": g_label,
                                       "widget_right": g_text,
                                       "value": g_text.text}

            # logging to verify widgets stores properly
            Logger.debug(f"{x}\n----")
            Logger.debug(f"Left Widget: {self.profile_widgets[x]['widget_left']}")
            Logger.debug(f"Right Widget: {self.profile_widgets[x]['widget_right']}\n----")

    def add_grid_Labels(self, name):
        """Create and return label for each value in profile_option []"""
        # size hint for each label
        size = (0.5, 1)
        grid_label = Button(text=name.title(), # title each word in option
                           size_hint=size)

        return grid_label

    def add_grid_textinput(self):
        """Create and return textinput box for each setting in profile_options[]"""
        size = (1,1)
        textinput = TextInput(multiline = False, size_hint = size)
        return textinput

    # Functions for updating the profile options
    # todo implement functionality for on_change values to update database table stat
    def on_change_slider(self):
        pass

    def on_change_age(self):
        pass

    def on_change_weight(self):
        pass

    def on_change_weightgoal(self):
        pass

    def on_change_gender(self):
        pass

    def on_change_height(self):
        print("Uhh you pressed enter")
        pass

    def update_profile(self):
        pass
class Screen1(BaseScreen):
    def __init__(self, **kwargs):
        super(Screen1, self).__init__(**kwargs)
        self.layout.add_widget(Label(text='This is Screen 1', size_hint_y=None, height=30, font_size=24))


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
        self.add_widget(MainDashboard(name='main_dashboard', manager_instance=self))
        self.add_widget(SettingsScreen(name='settings'))
        self.add_widget(ProfileScreen(name='profile'))
        self.add_widget(Screen1(name='screen_1'))
        
    def navigate_to_screen(self, screen_name):
        """
        Navigate to the specified screen.
        
        Args:
            screen_name (str): The name of the screen to navigate to.
        """
        def inner_function(instance):
            self.manage_screens(screen_name, 'add')
        return inner_function

    def manage_screens(self, screen_name, operation):
        if operation == 'add':
            # Ensure only permitted screens are added to the stack
            if self.is_authenticated and screen_name in ['login', 'register', 'register_login', 'onboarding']:
                return
            self.screen_stack.append(screen_name)
        elif operation == 'remove' and self.screen_stack:
            self.screen_stack.pop()
        self.current = screen_name

    def go_back(self, window, key, *args):
        if key == 27:  # The escape key corresponds to the Android back button
            # When stack is empty, navigate/add 'main_dashboard' to stack
            if not self.screen_stack:
                self.current = 'main_dashboard'
                self.screen_stack.append('main_dashboard')
                return True

# Remove the current screen from the stack
            self.screen_stack.pop()

# When stack is not empty, navigate to the next screen
            if self.screen_stack:
                next_screen = self.screen_stack[-1]

# Check if authenticated and if next screen is restricted
                if self.is_authenticated and next_screen in ['login', 'register', 'register_login', 'onboarding']:
# Clear screen stack and set current screen to 'main_dashboard'
                    self.screen_stack.clear()
                    self.screen_stack.append('main_dashboard')
                    self.current = 'main_dashboard'
                else:
                    # Set next screen as current and remove it from stac
                    self.current = next_screen
                    self.screen_stack.pop()
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
        db_manager = DatabaseManager("database.db")  # Initialize DatabaseManager
        db_manager.initialize_database()  # Initialize database
        sm = Manager()
        Window.bind(on_keyboard=sm.go_back) # bind back button
        sm.current = 'onboarding' # set the first screen
        sm.manage_screens('onboarding', 'add')
        return sm


Builder.load_file("C:\\Workout-Tracker-App\\app\\Kivy_files\\profile.kv")
Builder.load_file("C:\\Workout-Tracker-App\\app\\Kivy_files\\settings.kv")
# Main function to run the application
if __name__ == '__main__':
    """
    Entry point for the application. 
    Initializes and runs the Kivy app.
    """
    MyApp().run()
