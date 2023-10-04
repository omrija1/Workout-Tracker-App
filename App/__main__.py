# Inside __main__.py
if __name__ == '__main__':
    print("App is running!")

    # Logging setup
    import logging
    logging.basicConfig(filename='app.log', level=logging.DEBUG)

    # Environment Variables
    import os
    os.environ['DB_CONNECTION_STRING'] = 'C:\\Workout-Tracker-App\\database.db'
    
    # Database Initialization
    
    # Run the Kivy App

    from app.UIComponentsOrActivities.User_Onboarding_and_System_Initialization.kivy_interface import MyApp
    MyApp().run()

# Path: app/UIComponentsOrActivities/User_Onboarding_and_System_Initialization/kivy_interface.py