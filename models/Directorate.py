from peewee import *
from models.BaseModel import BaseModel, db
from models.City import City


class Directory(BaseModel):
    city_id = ForeignKeyField(model=City, backref="city")
    name = CharField(max_length=30)


db.create_tables([Directory])
