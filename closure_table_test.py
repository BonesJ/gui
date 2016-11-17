from peewee import *
from playhouse.sqlite_ext import *

db = SqliteExtDatabase('testdbclosure.db')
db.load_extension('./resources/closure/closure.dll')  # Note we leave off .so

class Category(Model):
    name = CharField()
    parent = ForeignKeyField('self', index=True, null=True)  # Required.

    class Meta:
        database = db

CategoryClosure = ClosureTable(Category)

# Create the tables if they do not exist.
db.create_tables([Category, CategoryClosure], True)