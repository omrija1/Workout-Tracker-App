import sqlite3
import os
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.screenmanager import ScreenManager, Screen
from ...Database.User_Account_Data import db_setup


class UserOnboarding(Screen):
    """Handles the initial onboarding screen.

    Attributes:
        layout: The main layout for this screen.
    """

    def __init__(self, **kwargs) -> None:
        """Initialize the UserOnboarding class and its widgets."""
        super(UserOnboarding, self).__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical')
        self.layout.add_widget(Label(text='Welcome!', size_hint_y=None, height=30, font_size=24))
        self.layout.add_widget(Button(text='Press to Continue', size_hint_y=None, height=50, on_press=self.show_register_login))
        self.add_widget(self.layout)

    def show_register_login(self, instance) -> None:
        """Navigate to the register/login screen."""
        self.manager.current = 'register_login'


class RegisterLogin(Screen):
    """Handles the Register or Login choice screen.

    Attributes:
        layout: The main layout for this screen.
    """

    def __init__(self, **kwargs) -> None:
        """Initialize the RegisterLogin class and its widgets."""
        super(RegisterLogin, self).__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical')
        self.layout.add_widget(Label(text='Choose an Option:', size_hint_y=None, height=30, font_size=18))
        self.layout.add_widget(Button(text='Register', size_hint_y=None, height=50, on_press=self.show_register_form))
        self.layout.add_widget(Button(text='Login', size_hint_y=None, height=50, on_press=self.show_login_form))
        self.add_widget(self.layout)

    def show_register_form(self, instance) -> None:
        """Navigate to the registration screen."""
        self.manager.current = 'register'

    def show_login_form(self, instance) -> None:
        """Navigate to the login screen."""
        self.manager.current = 'login'


class RegisterScreen(Screen):
    """Handles the user registration screen.

    Attributes:
        layout: The main layout for this screen.
    """

    def __init__(self, **kwargs) -> None:
        """Initialize the RegisterScreen class and its widgets."""
        super(RegisterScreen, self).__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical')
        # Existing widgets for registration form
        self.username = TextInput(hint_text='Username', size_hint_y=None, height=30)
        self.email = TextInput(hint_text='Email', size_hint_y=None, height=30)
        self.password = TextInput(hint_text='Password', password=True, size_hint_y=None, height=30)
        self.layout.add_widget(self.username)
        self.layout.add_widget(self.email)
        self.layout.add_widget(self.password)
        self.layout.add_widget(Button(text='Submit', size_hint_y=None, height=50, on_press=self.register_user))
        self.add_widget(self.layout)

    def register_user(self, instance) -> None:
        """Register a new user."""
        result = db_setup.add_user(self.username.text, self.email.text, self.password.text)
        self.layout.clear_widgets()
        self.layout.add_widget(Label(text=str(result.get('message', result)), size_hint_y=None, height=30, font_size=18))


class LoginScreen(Screen):
    """Handles the user login screen.

    Attributes:
        layout: The main layout for this screen.
    """

    def __init__(self, **kwargs) -> None:
        """Initialize the LoginScreen class and its widgets."""
        super(LoginScreen, self).__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical')
        self.email = TextInput(hint_text='Email', size_hint_y=None, height=30)
        self.password = TextInput(hint_text='Password', password=True, size_hint_y=None, height=30)
        self.layout.add_widget(self.email)
        self.layout.add_widget(self.password)
        self.layout.add_widget(Button(text='Submit', size_hint_y=None, height=50, on_press=self.login_user))
        self.add_widget(self.layout)

    def login_user(self, instance) -> None:
        """Handle user login."""
        db_connection_string = os.environ.get('DB_CONNECTION_STRING', 'C:\\Workout-Tracker-App\\database.db')
        conn = sqlite3.connect(db_connection_string)
        if db_setup.verify_login(self.email.text, self.password.text, conn):
            self.layout.clear_widgets()
            self.layout.add_widget(Label(text="Login successful.", size_hint_y=None, height=30, font_size=18))
        else:
            self.layout.clear_widgets()
            self.layout.add_widget(Label(text="Invalid email or password.", size_hint_y=None, height=30, font_size=18))


class Manager(ScreenManager):
    """Manages all the screens and transitions."""

    def __init__(self, **kwargs) -> None:
        """Initialize the screen manager."""
        super(Manager, self).__init__(**kwargs)
        self.add_widget(UserOnboarding(name='onboarding'))
        self.add_widget(RegisterLogin(name='register_login'))
        self.add_widget(RegisterScreen(name='register'))
        self.add_widget(LoginScreen(name='login'))


class MyApp(App):
    """The main application class."""

    def build(self) -> Manager:
        """Builds the application interface."""
        db_setup.initialize_database("database.db")
        return Manager()


if __name__ == '__main__':
    MyApp().run()
