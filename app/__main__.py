from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from sqlalchemy.orm import Session
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRaisedButton
from app.Database.models import Exercise, engine
from kivymd.toast import toast
from kivymd.uix.dialog import MDDialog
from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDIconButton
from kivymd.app import MDApp



Builder.load_string("""
<CreateExerciseScreen>:
    name: 'create_exercise'
    BoxLayout:
        orientation: 'vertical'
        MDTextField:
            id: exercise_name
            hint_text: 'Exercise Name'
        MDTextField:
            id: main_muscle_group
            hint_text: 'Main Muscle Group'
        MDTextField:
            id: secondary_muscle_groups
            hint_text: 'Secondary Muscle Groups (comma separated)'
        MDTextField:
            id: sets
            hint_text: 'Sets'
        MDTextField:
            id: reps
            hint_text: 'Reps'
        MDTextField:
            id: rest_time
            hint_text: 'Rest Time (in seconds)'
        MDTextField:
            id: training_method
            hint_text: 'Training Method (Normal Sets or Super Set)'
        MDRaisedButton:
            text: 'Save Exercise'
            on_release: app.save_exercise()
""")

class CreateExerciseScreen(MDScreen):
    def save_exercise(self):
        # Retrieve inputs from the UI
        name = self.ids.exercise_name.text.strip()
        main_muscle_group = self.ids.main_muscle_group.text.strip()
        secondary_muscle_groups = self.ids.secondary_muscle_groups.text.strip()
        sets = self.ids.sets.text.strip()
        reps = self.ids.reps.text.strip()
        rest_time = self.ids.rest_time.text.strip()
        training_method = self.ids.training_method.text.strip()
        
        try:
            sets = int(sets)
            reps = int(reps)
            rest_time = int(rest_time)
            assert 0 < sets <= 30  # Example condition: sets should be between 1 and 30
            assert 0 < reps <= 250  # Example condition: reps should be between 1 and 250
            assert training_method in ['Normal Sets', 'Super Set']
            assert name and main_muscle_group  # Ensure these fields are not empty
        except (ValueError, AssertionError) as e:
            return

        # Create an Exercise instance
        exercise = Exercise(
            name=name,
            main_muscle_group=main_muscle_group,
            secondary_muscle_groups=secondary_muscle_groups,
            sets=sets,
            reps=reps,
            rest_time=rest_time,
            training_method=training_method
        )

        # Save to the database
        with Session(engine) as session:
            session.add(exercise)
            try:
                session.commit()
                toast('Exercise saved successfully.')
            except Exception as e:
                session.rollback()
                self.show_error_dialog(str(e))

    def show_error_dialog(self, message):
        dialog = MDDialog(title='Error', text=message)
        dialog.open()




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
        from app.Database.db_setup import DatabaseManager
        db_manager = DatabaseManager('database.db')
        db_manager.initialize_database()
        
        # Run the Kivy App
        from app.kivy_interface_alch import MyApp
        MyApp().run()

    except Exception as e:
        logging.exception("Exception occurred")