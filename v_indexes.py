from sqlmodel import Index
from db import engine
# indexes are pretty much just a convenient and efficient way of selecting data from a db. it works in the same way  as finding data in a dictionary
# so if you have queries that find records by a specific column, it makes sense to add an index for that column to reduce the number of operations

# CREATE INDEX ix_hero_name
# ON hero (name)
# Hey SQL database 👋, please CREATE an INDEX for me.
# I want the name of the index to be ix_hero_name.
# This index should be ON the table hero, it refers to that table.
# The column I want you to use for it is name.

# but this indexes have their own down side in terms of space and computation

# to know more https://sqlmodel.tiangolo.com/tutorial/indexes/

from typing import Optional

from sqlmodel import Field, Session, SQLModel, create_engine, select


class Hero(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    # tell SQLModel to create an index for the name field when creating the table:
    # SQLModel (actually SQLAlchemy) will automatically generate the index name for you.
    # In this case the generated name would be ix_hero_name.

    name: str = Field(index=True)
    secret_name: str
    age: Optional[int] = Field(default=None, index=True)

# Now, to query the data using the field name and the new index we don't have to do anything special or different in the code, it's just the same code.
# So, when we query the database for the hero table and use those two columns to define what data we get, the database will be able to use those indexes to improve the reading performance.
# You probably noticed that we didn't set index=True for the id field.
# Because the id is already the primary key, the database will automatically create an internal index for it.
# The database always creates an internal index for primary keys automatically, as those are the primary way to organize, store, and retrieve data. 🤓
# But if you want to be frequently querying the SQL database for any other field (e.g. using any other field in the WHERE section), you will probably want to have at least an index for that.


def select_heroes():
    with Session(engine) as session:
        statement = select(Hero).where(Hero.name == "Deadpond")
        results = session.exec(statement)
        for hero in results:
            print(hero)


select_heroes()
