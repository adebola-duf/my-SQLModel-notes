from sqlmodel import SQLModel, Session
from models import Hero
from db import engine

engine.echo = False


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def create_heroes():
    # Because we don't set the id, it takes the Python's default value of None that we set in Field(default=None).
    # If we assumed that the id was always an int and added the type annotation without Optional, we could end up writing broken code, like:
    # next_hero_id = hero_1.id + 1
    # But by declaring it with Optional[int], the editor will help us to avoid writing broken code by showing us a warning telling us that the code could be invalid if hero_1.id is None. 🔍
    hero_1 = Hero(name="Deadpond", secret_name="Dive Wilson", id=32)
    hero_2 = Hero(name="Spider-Boy", secret_name="Pedro Parqueador", id=239)
    hero_3 = Hero(name="Rusty-Man", secret_name="Tommy Sharp", age=48)

    print("Before interacting with the database")
    # The id in all these hero instances would still be None because of the default=None
    print("Hero 1:", hero_1)
    print("Hero 2:", hero_2)
    print("Hero 3:", hero_3)

    with Session(engine) as session:
        session.add(hero_1)
        session.add(hero_2)
        session.add(hero_3)
        # Even after adding the rows to the session, the instance would still be None because the session is smart and doesn't talk to the database every time we prepare something to be changed, only after we are ready and tell it to commit the changes it goes and sends all the SQL to the database to store the data.
        print("After adding to the session")
        print("Hero 1:", hero_1)
        print("Hero 2:", hero_2)
        print("Hero 3:", hero_3)

        session.commit()

        # After committing the session, if you try printing the heroes, you won't get anything (Hero 1: ). And the reason why is because SQLModel is internally marking
        # these objects as expired they don't have the latest version of their data. This is because we could have some fields updated in the database, for example, imagine a field updated_at: datetime that was automatically updated when we saved changes.
        print("After committing the session")
        print("Hero 1:", hero_1)
        print("Hero 2:", hero_2)
        print("Hero 3:", hero_3)

        # but the funny thing is that after committing the session, if we try and access single fields, SQLModel (actually SQLAlchemy) will make sure to contact the database and get the most recent version of the data, updating that field name in our object and then making it available for the rest of the Python expression
        print("After committing the session, show IDs")
        print("Hero 1 ID:", hero_1.id)
        print("Hero 2 ID:", hero_2.id)
        print("Hero 3 ID:", hero_3.id)

        # But if we want to explicitly refresh the data, - session.refresh(object)
        # the session goes and makes the engine communicate with the database to get the recent data for this object hero_1, and then the session puts the data in the hero_1 object and marks it as "fresh" or "not expired".
        session.refresh(hero_1)
        session.refresh(hero_2)
        session.refresh(hero_3)

        print("After refreshing the heroes")
        print("Hero 1:", hero_1)
        print("Hero 2:", hero_2)
        print("Hero 3:", hero_3)
    print("After the session closes. NB: Even if we don't explicitly refresh it, it refreshes automtically when the session closes")
    print("Hero 1:", hero_1)
    print("Hero 2:", hero_2)
    print("Hero 3:", hero_3)


def main():
    create_db_and_tables()
    create_heroes()


if __name__ == "__main__":
    main()
