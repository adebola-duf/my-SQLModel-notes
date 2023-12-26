from sqlmodel import SQLModel, Session
from models import Hero
from db import engine


def create_db_and_tables():
    # If the database and table already exists, then it is just going to insert the data into the already existing table It doesn't overwrite it
    SQLModel.metadata.create_all(engine)

# data is either in memory or is in the database\
# what we want to do is create data in memory and then save send it to the database

# INSERT INTO "hero" ("name", "secret_name")
# VALUES ("Deadpond", "Dive Wilson");


def create_heroes():
    # Each instance we create will represent the data in a row in the database.
    hero_1 = Hero(name="Deadpond", secret_name="Dive Wilson")
    hero_2 = Hero(name="Spider-Boy", secret_name="Pedro Parqueador")
    hero_3 = Hero(name="Rusty-Man", secret_name="Tommy Sharp", age=48)

    # In contrast to the engine that we create once for the whole application, we create a new session for each group of operations with the database that belong together.
    with Session(engine) as session:
        # The session is holding in memory all the objects that should be saved in the database later.
        # And once we are ready, we can commit those changes, and then the session will use the engine underneath to save all the data by sending the appropriate SQL to the database, and that way it will create all the rows. All in a single batch.
        session.add(hero_1)
        session.add(hero_2)
        session.add(hero_3)
        session.commit()


def main():
    create_db_and_tables()
    create_heroes()


if __name__ == "__main__":
    main()
