from peewee import *
from db import *
from School import School
import datetime


# from users import Users
class Device(BaseModel):
    school_id = ForeignKeyField(model=School, backref='Devices')
    name = CharField(max_length=30)
    ip = CharField(max_length=20)
    port = IntegerField()
    status = CharField(max_length=20)
    password = CharField(max_length=30)


db.create_tables([Device])
