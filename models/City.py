from peewee import *
from models.BaseModel import BaseModel


class City(BaseModel):
    name = CharField(max_length=20)


# db.create_tables([City])
