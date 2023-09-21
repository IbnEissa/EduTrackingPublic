from peewee import *
from models.BaseModel import BaseModel ,db
from models.School import School
from models.Teachers import Teachers


class ClassRoom(BaseModel):
    school_id = ForeignKeyField(model=School, backref="Users")
    name = CharField(max_length=20, unique=True)
    class_leader = ForeignKeyField(model=Teachers, backref='classes')


db.create_tables([ClassRoom])
