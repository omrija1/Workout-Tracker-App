# Inside __main__.py
if __name__ == '__main__':
    print("App is running!")

    # Logging setup
    import logging
    logging.basicConfig(filename='app.log', level=logging.DEBUG)

    # Environment Variables
    import os
    os.environ['DB_CONNECTION_STRING'] = 'C:\\Workout-Tracker-App\\database.db'
    
    try:
        # Database Initialization
        from app.database.db_setup import DatabaseManager
        db_manager = DatabaseManager('database.db')
        db_manager.initialize_database()
        
        # Run the Kivy App
        from app.kivy_interface import MyApp
        MyApp().run()

    except Exception as e:
        logging.exception("Exception occurred")