from sqlmodel import Session, select, or_, col
from models import Hero
from db import engine
engine.echo = False


def select_heroes():
    with Session(engine) as session:
        statement = select(Hero).where(
            or_(col(Hero.age) == 18, Hero.name == "Deadpond"))
        # This results is an iterable. But if we want to get our rows as a list we do
        results = session.exec(statement)
        # for hero in results:
        #     print(hero)

        # list_results = results.all()
        # print("list results:", list_results)

        # if we are only interested in the first row returned, we do. And if no row matches our query, it returns None
        # hero = results.first()
        # print("hero:", hero)

        # There might be cases where we want to ensure that there's exactly one row matching the query. And if there was more than one, it would mean that there's an error in the system, and we should terminate with an error.
        # from sqlalchemy import exc
        # exc.MultipleResultsFound
        # Also in a case where we want to ensure only one row matches the query and no row is returned, it raises a exc.NoResultFound
        # hero = results.one()
        # print("Hero:", hero)

        # A more compact version of all these
        hero = session.exec(select(Hero).where(col(Hero.age) == 18)).one()
        print("Her0:", hero)

        # IF you want to get a single row by the primary key which will always give you a primary key. you can use the first or one. But there is a shorter version
        hero = session.get(Hero, 240)
        print("Hero:", hero)
        # .get() behaves similar to .first(), if there's no data it will simply return None (instead of raising an error):


select_heroes()
