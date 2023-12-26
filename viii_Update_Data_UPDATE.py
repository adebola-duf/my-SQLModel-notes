from sqlmodel import Session, select
from models import Hero
from db import engine
engine.echo = False
# UPDATE hero
# SET age=16
# WHERE name = "Spider-Boy"


def update_heroes():
    with Session(engine) as session:
        statement = select(Hero).where(Hero.name == "Spider-Boy")
        results = session.exec(statement)
        hero = results.one()
        print("Hero:", hero)

        hero.age = 16
        # Now that the hero object in memory has a change, in this case a new value for the age, we need to add it to the session.
        session.add(hero)
        # To save the current changes in the session, commit it. This will save the updated hero in the database:
        session.commit()
        session.refresh(hero)
        print("Updated hero:", hero)

        statement = select(Hero).where(Hero.name == "Spider-Boy")
        results = session.exec(statement)
        hero_1 = results.one()
        print("Hero 1:", hero_1)

        statement = select(Hero).where(Hero.name == "Captain North America")
        results = session.exec(statement)
        hero_2 = results.one()
        print("Hero 2:", hero_2)

        hero_1.age = 16
        hero_1.name = "Spider-Youngster"
        session.add(hero_1)

        hero_2.name = "Captain North America Except Canada"
        hero_2.age = 110
        session.add(hero_2)

        session.commit()
        session.refresh(hero_1)
        session.refresh(hero_2)


update_heroes()
