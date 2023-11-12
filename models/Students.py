from peewee import *
from models.BaseModel import BaseModel, db
from models.Members import Members
import datetime
from models.ClassRoom import ClassRoom


class Students(BaseModel):
    member_id = ForeignKeyField(model=Members, backref="member_id")
    # class_id = CharField()
    class_id =  ForeignKeyField(model=ClassRoom, backref="class_id")


db.create_tables([Students])
