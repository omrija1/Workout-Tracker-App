from sqlalchemy import String, Column, TEXT, Integer, create_engine, DATE,ForeignKey
from sqlalchemy.orm import declarative_base, Mapped, mapped_column, Session, sessionmaker, Mapped, mapped_column, \
    relationship
from datetime import datetime
import uuid

# from db_setup_alch import Base
"<dialect>+<driver>://<username>:<password>@<host>:<port>/<database>"
sql3_url = "sqlite3://root:pass@127.0.0.1:8080/database"
db_url_m = "sqlite://:memory:"
# 3 relative path 4 absolute path

db_url = "sqlite:///..//database2.db"
"sqlite://:memory:"

Base = declarative_base()
engine = create_engine(db_url)
Session = sessionmaker(bind=engine)
session = Session()


def generate_uuid():
    return str(uuid.uuid4())


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
        self.created_ts = datetime.today().date()
        self.quote = ""
        self.author = ""
        self.last_displayed = None

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
        self.last_displayed = datetime.today().date()



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
    gender: Mapped[int]
    age: Mapped[int]

    # Stats init F(n)
    def __init__(self, id, height="", weight="", weight_goal="", gender="", age=""):
        """ Init Function: Stats tables
            -: only username is initially requierd upon creation
        """
        self.id = id
        self.height = height
        self.weight = weight
        self.weight_goal = weight_goal
        self.gender = gender
        self.age = age

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



def create_db():
    """Function to create the database"""
    # Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)


# create engine - passes database url paramater
# engine = create_engine(database_url)


