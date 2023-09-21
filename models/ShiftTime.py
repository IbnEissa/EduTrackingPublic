from peewee import *
from db import *


# from datetime import time


class ShiftTime(BaseModel):
    name = CharField(max_length=50)
    shift_Type = CharField(max_length=50)
    beginning_attendance = TimeField()
    end_attendance = TimeField()
    Beginning_departure = TimeField()
    End_departure = TimeField()
    amount_shift = FloatField()


db.create_tables([ShiftTime])
