from peewee import *
from database import db

class BaseModel(Model):
    class Meta:
        database = db

class Author(BaseModel):
    name = CharField()
    email = CharField(unique=True)

class Post(BaseModel):
    title = CharField()
    content = TextField()
    author = ForeignKeyField(Author, backref="posts", on_delete="CASCADE")
