from peewee import *
from db import *


class SystemScreens(BaseModel):
    name = CharField(max_length=40)
    system_fr = CharField(max_length=40)
    additional = CharField(max_length=40)


db.create_tables([SystemScreens])
