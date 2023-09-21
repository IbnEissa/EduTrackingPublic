from peewee import *
from db import *


class Days(BaseModel):
    name = CharField(max_length=20)


db.create_tables([Days])
