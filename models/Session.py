from peewee import *
# from db import *
from models.BaseModel import BaseModel, db



class Session(BaseModel):
    name = CharField(max_length=20)
    start_time = TimeField()
    end_time = TimeField()


db.create_tables([Session])
