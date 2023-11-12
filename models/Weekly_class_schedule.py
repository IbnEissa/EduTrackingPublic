from peewee import *
# from db import *
from models.Session import Session
# from Days import Days
# from Users import Users
# from teacher import Teacher
from models.Members import Members
from models.Subjects import Subjects
from models.ClassRoom import ClassRoom
from models.BaseModel import BaseModel, db



class WeeklyClassSchedule(BaseModel):
    teacher_id = ForeignKeyField(model=Members, backref="Teacher")
    subject_id = ForeignKeyField(model=Subjects, backref="Subjects")
    class_room_id = ForeignKeyField(model=ClassRoom, backref="Class_room")
    # day_id = ForeignKeyField(model=Days, backref='Teacher_Subjects')
    session_id = ForeignKeyField(model=Session, backref='Teacher_Subjects')
    # class  Meta:
    #      primary_key = CompositeKey('teacher_id',  'session_id','day_id')


db.create_tables([WeeklyClassSchedule])
