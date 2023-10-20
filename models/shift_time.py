from peewee import *
from models.db import *
# from datetime import time
import datetime


class Shift_time(BaseModel):
    name = CharField(max_length=50)
    shift_Type = CharField(max_length=50)
    start_time = TimeField()
    delay_times = IntegerField()
    end_time = TimeField()
    created_at = DateTimeField(default=datetime.datetime.now)
    updated_at = DateTimeField(default=datetime.datetime.now)


db.create_tables([Shift_time, ])
