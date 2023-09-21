from peewee import *
from db import *


class Subjects(BaseModel):
    name = CharField(max_length=70)


db.create_tables([Subjects])
