from sqlalchemy import String, Column, Integer, create_engine, DATE,ForeignKey
from sqlalchemy.orm import relationship, mapped_column, sessionmaker, Mapped, mapped_column
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import uuid



Base = declarative_base()



def generate_uuid():
    return str(uuid.uuid4())



class Exercise(Base):
    __tablename__ = 'exercises'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    main_muscle_group = Column(String, nullable=False)
    secondary_muscle_groups = Column(String)  # Assuming this is a comma-separated string
    sets = Column(Integer, nullable=False)
    reps = Column(Integer, nullable=False)
    rest_time = Column(Integer, nullable=False)  # Assuming rest time is in seconds
    training_method = Column(String, nullable=False)




class Quotes(Base):
    """Quotes Table"""
    __tablename__ = "quotes"
    id: Mapped[int] = mapped_column(primary_key=True)
    quote: Mapped[str]
    author: Mapped[str]

    def __init__(self, quote, author):
        self.quote = quote
        self.author = author

    def display_quote(self):
        print(f"id: {self.id}")
        print(f"Quote: {self.quote}")
        print(f"Author: {self.author}\n")




class Profile(Base):
    """Profile Table"""
    __tablename__ = "profile"

    # user_id - order user entered
    user_id = Column("user_id", Integer, default = 1)

    # id - primary key
    id: Mapped[str] = mapped_column(default=generate_uuid, primary_key=True)

    username: Mapped[str]
    email: Mapped[str]
    password: Mapped[str]
    created_ts: Mapped[datetime]
    quote: Mapped[str]
    author: Mapped[str]
    last_displayed: Mapped[datetime] = mapped_column(nullable=True)

    # Profile Init F(n)
    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password
        self.created_ts = datetime.now()
        self.quote = ""
        self.author = ""
        self.last_displayed = datetime.min

    # Profile print function
    def display_user(self):
        print(f"id: {self.id}")
        print(f"username: {self.id}")
        print(f"email: {self.email}")
        print(f"password: {self.password}")
        print(f"created: {self.created_ts}")

    def update_quote(self, quote, author):
        self.quote = quote
        self.author = author
        self.last_displayed = datetime.now()



class Stats(Base):
    """Stats Table"""
    __tablename__ = "stats"

    # Primary key
    stats_id: Mapped[int] = mapped_column(primary_key=True)

    # id mapped to profile table
    id: Mapped[str] = mapped_column("id", String, ForeignKey("profile.id"))

    # Foreign Key to Profile table

    # Stats Content
    height: Mapped[str]
    weight: Mapped[str]
    weight_goal: Mapped[int]
    gender: Mapped[str]
    age: Mapped[int]

    # Stats init F(n)
    def __init__(self, id, height="", weight="", weight_goal="", gender="", age=""):
        """ Init Function: Stats tables
            -: only username is initially requierd upon creation
        """
        self.id = id
        self.height = height
        self.weight = weight
        self.weight_goal = int(weight_goal)
        self.gender = str(gender)
        self.age = int(age)

    def display_stat(self):
        print(f"Stat_id: {self.stats_id}")
        print(f"id: {self.id}")


class Library(Base):
    """Library Table"""
    __tablename__ = "library"
    id = Column("id", Integer, primary_key=True)
    pass




class Quote_Display(Base):
    """
    Quote Display table
    -This table contains the last displayed quote for a user
    """
    __tablename__ = "quote_display"
    id = Column("id", Integer, primary_key=True)
    last_displayed = Column("last_displayed", DATE)
    quote = Column("quote", String)
    author = Column("author", String)

    def __init__(self, quote, author, current_date=""):

        # Generate Current Date Format MM-DD-YYYY
        current_date = datetime.today().date()
        self.date = current_date
        self.quote = quote
        self.author = author

engine = create_engine('sqlite:///C:\\\\Workout-Tracker-App\\\\database.db')
def create_db():
    """Function to create the database"""
    # Base.metadata.drop_all(engine)
    # Base.metadata.create_all(engine)



    # Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)


