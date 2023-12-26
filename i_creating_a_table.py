from typing import Annotated, Optional
from sqlmodel import SQLModel, Field, create_engine
import os
from dotenv import load_dotenv
load_dotenv()
# This class Hero represents the table for our heroes. And each instance we create later will represent a row in the table.
# We use the config table=True to tell SQLModel that this is a table model, it represents a table.
# without the table=True, this Hero class would be treated as a data model. More on that later


class Hero(SQLModel, table=True):
    # These class attributes represent the columns in our table
    # id here is our primary key
    # Bola if it is the primary key, why are we making it "nullable"? Well
    # The reason why is that this field is required in the database but it is generated by the database. I feel what this place is talking about is that the id field can't be null.
    # So if we make it null, the database generates a value for us. But if we pass a value, the database would use the value we passed. This is correct (message from future me)
    # so when we create a new instance(row) and we don't pass in the value of the id, it's value would be None until we save it in the database and then it will finnally have a value automatically generated by the database
    id: Annotated[int | None, Field(primary_key=True)] = None
    name: str
    secret_name: str
    # Optional is a way of saying that a variable can either be int or none. It is equivalent to saying int | None
    # By making this age column of type int or null, it means it is not required when validating the data. and by making the default
    # None, we are telling SQLModel that the default value of age in the database should be Null the SQL equivalent to python's None
    age: Optional[int] = None  # age is a nullable column


# The engine is an object used to handle communications to the database
sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"
postgres_url = os.getenv("POSTGRES_DB_URL")
# It will make the engine print all the SQL statements it executes. But in production, you might want to tremove this echo=True
engine = create_engine(url=postgres_url, echo=True)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
# it creates the database.db file and creates the hero table in that database.
# The SQLModel class has a metadata attribute. It is an instance of a class MetaData.
# Whenever you create a class that inherits from SQLModel and is configured with table = True, it is registered in this metadata attribute.
# So, by the last line, SQLModel.metadata already has the Hero registered.
# This MetaData object at SQLModel.metadata has a create_all() method.
# It takes an engine and uses it to create the database and all the tables registered in this MetaData object.

# This also means that you have to call SQLModel.metadata.create_all() after the code that creates new model classes inheriting from SQLModel.
# For example, let's imagine you do this:
# Create the models in one Python file models.py.
# Create the engine object in a file db.py.
# Create your main app and call SQLModel.metadata.create_all() in app.py.
# If you only imported SQLModel and tried to call SQLModel.metadata.create_all() in app.py, it would not create your tables:


# # This wouldn't work! 🚨
# from sqlmodel import SQLModel

# from .db import engine

# SQLModel.metadata.create_all(engine)
# It wouldn't work because when you import SQLModel alone, Python doesn't execute all the code creating the classes inheriting from it (in our example, the class Hero), so SQLModel.metadata is still empty.
# But if you import the models before calling SQLModel.metadata.create_all(), it will work:
# from sqlmodel import SQLModel

# from . import models
# from .db import engine

# SQLModel.metadata.create_all(engine)
# This would work because by importing the models, Python executes all the code creating the classes inheriting from SQLModel and registering them in the SQLModel.metadata.

# As an alternative, you could import SQLModel and your models inside of db.py:

if __name__ == "__main__":
    create_db_and_tables()
