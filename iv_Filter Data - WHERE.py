from sqlmodel import Session, select, or_, col
from db import engine
from models import Hero

# SELECT id, name, secret_name, age
# FROM hero
# WHERE name = "Deadpond"
# SELECT is used to tell the SQL database what columns to return.
# WHERE is used to tell the SQL database what rows to return.


def select_heroes():
    with Session(engine) as session:
        # Model class attributes for each of the columns/fields are special and can be used for expressions.
        # But that's only for the model class attributes. Instance attributes behave like normal Python values.
        # Hero.name == "Deadpond"
        # ...results in one of those expression objects to be used with .where():
        # <sqlalchemy.sql.elements.BinaryExpression object at 0x7f4aec0d6c90>
        # But if you take an instance:
        # some_hero = Hero(name="Deadpond", secret_name="Dive Wilson")
        # ...and use it in a comparison:
        # some_hero.name == "Deadpond"
        # ...that results in a Python value of:
        # True

        # select(Hero).where(Hero.name == hero.name) This is very valid
        engine.echo = False
        statement = select(Hero).where(Hero.age >= 18)
        # SELECT id, name, secret_name, age
        # FROM hero
        # WHERE age >= 18 AND name == Bolexyro
        statement = select(Hero).where(
            Hero.age >= 18).where(Hero.name == "Bolexyro")
        # or we could do
        statement = select(Hero).where(
            Hero.age >= 18, Hero.name == "Bolexyro")

        # SELECT id, name, secret_name, age
        # FROM hero
        # WHERE age >= 18 OR name == Bolexyro
        statement = select(Hero).where(
            or_(Hero.age >= 18, Hero.name == "Deadpond"))

        results = session.exec(statement)
        for hero in results:
            print(hero)

        # There's a chance that your editor gives you an error when using these comparisons, like:
        # Hero.age > 35
        # It would be an error telling you that
        # Hero.age is potentially None, and you cannot compare None with >
        # This is because as we are using pure and plain Python annotations for the fields, age is indeed annotated as Optional[int], which means int or None.
        # By using this simple and standard Python type annotations we get the benefit of the extra simplicity and the inline error checks when creating or using instances. ✨
        # And when we use these special class attributes in a .where(), during execution of the program, the special class attribute will know that the comparison only applies for the values that are not NULL in the database, and it will work correctly.
        # But the editor doesn't know that it's a special class attribute, so it tries to help us preventing an error (that in this case is a false alarm).
        # Nevertheless, we can easily fix. 🎉
        # We can tell the editor that this class attribute is actually a special SQLModel column (instead of an instance attribute with a normal value).
        # To do that, we can import col() (as short for "column"):
        statement = select(Hero).where(
            or_(col(Hero.age) >= 18, Hero.name == "Deadpond"))
        results = session.exec(statement)
        for hero in results:
            print(hero)


if __name__ == "__main__":
    select_heroes()
