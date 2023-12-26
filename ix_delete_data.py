from sqlmodel import Session, select
from models import Hero
from db import engine
# DELETE
# FROM hero
# WHERE name = "Spider-Youngster"
# If you want to "delete" a single value in a column while keeping the row, you would instead update the row and that specific column value to null

# Code above omitted 👆


def delete_heroes():
    with Session(engine) as session:
        statement = select(Hero).where(Hero.name == "Spider-Youngster")
        results = session.exec(statement)
        hero = results.one()
        print("Hero: ", hero)

        session.delete(hero)
        session.commit()

        print("Deleted hero:", hero)

        statement = select(Hero).where(Hero.name == "Spider-Youngster")
        results = session.exec(statement)
        hero = results.first()

        if hero is None:  # this gets printed since the row ain't in the database any longer
            print("There's no hero named Spider-Youngster")

# Code below omitted 👇
