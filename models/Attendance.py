# from DatabaseConfigration import *
from peewee import *
from models.BaseModel import BaseModel, db
from models.Teachers import Teachers


class AttendanceModel(BaseModel):
    teacher_id = ForeignKeyField(model=Teachers, backref='attendances')
    device_number = CharField(max_length=50)
    out_time = DateTimeField()
    input_time = DateTimeField()
    status = CharField(max_length=15)
    punch = CharField(max_length=50)


# db.create_tables([AttendanceModel])
