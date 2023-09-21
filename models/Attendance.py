from peewee import *
from db import *
from Teachers import Teachers


class Attendance(BaseModel):
    teacher_id = ForeignKeyField(model=Teachers, backref='attendances')
    device_number = CharField(max_length=50)
    out_time = DateTimeField()
    input_time = DateTimeField()
    status = CharField(max_length=15)
    punch = CharField(max_length=50)


db.create_tables([Attendance])
