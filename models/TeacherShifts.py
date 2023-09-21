from peewee import *
from db import *
from Teachers import Teachers
from ShiftTime import ShiftTime


class TeacherShifts(BaseModel):
    teacher_id = ForeignKeyField(model=Teachers, backref="Teacher_id")
    shift_time_id = ForeignKeyField(model=ShiftTime, backref="shift_time_id")


db.create_tables([TeacherShifts])
