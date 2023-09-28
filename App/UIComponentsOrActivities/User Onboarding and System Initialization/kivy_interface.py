import sqlite3
import hashlib
import re
import sys
sys.path.append("C:\\Workout-Tracker-App\\App\\Database\\User Account Data")
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from db_setup import initialize_database, add_user, verify_login # Importing functions from db_setup




# Validate Email and Password
def validate_email_password(email, password):
    email_valid = re.match(r"[^@]+@[^@]+\.[^@]+", email)
    password_strong = len(password) >= 8
    return email_valid and password_strong

# Add User
def add_user(username, email, password):
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

# Verify Login
def verify_login(email, password):
    conn = sqlite3.connect('user_profiles.db')
    c = conn.cursor()
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    c.execute("SELECT * FROM profiles WHERE email=? AND password=?", (email, hashed_password))
    user = c.fetchone()
    conn.close()
    return bool(user)

# Kivy Interface
class UserOnboarding(BoxLayout):
    
    def __init__(self, **kwargs):
        super(UserOnboarding, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.add_widget(Label(text='Welcome!', size_hint_y=None, height=30, font_size=24))
        self.add_widget(Button(text='Press to Continue', size_hint_y=None, height=50, on_press=self.show_register_login))
        
    def show_register_login(self, instance):
        self.clear_widgets()
        self.add_widget(Label(text='Choose an Option:', size_hint_y=None, height=30, font_size=18))
        self.add_widget(Button(text='Register', size_hint_y=None, height=50, on_press=self.show_register_form))
        self.add_widget(Button(text='Login', size_hint_y=None, height=50, on_press=self.show_login_form))
        
    def show_register_form(self, instance):
        self.clear_widgets()
        self.username = TextInput(hint_text='Username', size_hint_y=None, height=30)
        self.email = TextInput(hint_text='Email', size_hint_y=None, height=30)
        self.password = TextInput(hint_text='Password', password=True, size_hint_y=None, height=30)
        self.add_widget(self.username)
        self.add_widget(self.email)
        self.add_widget(self.password)
        self.add_widget(Button(text='Submit', size_hint_y=None, height=50, on_press=self.register_user))
        
    def register_user(self, instance):
        result = add_user(self.username.text, self.email.text, self.password.text)
        self.clear_widgets()
        self.add_widget(Label(text=result, size_hint_y=None, height=30, font_size=18))
        
    def show_login_form(self, instance):
        self.clear_widgets()
        self.email = TextInput(hint_text='Email', size_hint_y=None, height=30)
        self.password = TextInput(hint_text='Password', password=True, size_hint_y=None, height=30)
        self.add_widget(self.email)
        self.add_widget(self.password)
        self.add_widget(Button(text='Submit', size_hint_y=None, height=50, on_press=self.login_user))
        
    def login_user(self, instance):
        if verify_login(self.email.text, self.password.text):
            self.clear_widgets()
            self.add_widget(Label(text="Login successful.", size_hint_y=None, height=30, font_size=18))
        else:
            self.clear_widgets()
            self.add_widget(Label(text="Invalid email or password.", size_hint_y=None, height=30, font_size=18))

class MyApp(App):
    
    def build(self):
        return UserOnboarding()


if __name__ == '__main__':
    MyApp().run()
