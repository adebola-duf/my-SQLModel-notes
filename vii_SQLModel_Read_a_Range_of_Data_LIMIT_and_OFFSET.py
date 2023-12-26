from sqlmodel import Session, select
from models import Hero
from db import engine

engine.echo = False
# limit - to limit the number of rows returned. So lets say our query was originally meant to return 7 rows. if we make the limit somn like 3, then it would only return the first 3 rows
# offset - this skips the number of specified rows


def select_heroes():
    with Session(engine) as session:
        statement = select(Hero).limit(3)
        results = session.exec(statement)
        heroes = results.all()
        print(heroes)

        # Now we are going to skip the first 3 rows. and even if the remainng rows are not up to 3, the limit(3) wont raise any error
        statement = select(Hero).offset(5).limit(3)
        results = session.exec(statement)
        heroes = results.all()
        print(heroes)


select_heroes()
