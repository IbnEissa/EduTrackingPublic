from peewee import *
from db import *


class Session(BaseModel):
    name = CharField(max_length=20)
    start_time = TimeField()
    end_time = TimeField()


db.create_tables([Session])
