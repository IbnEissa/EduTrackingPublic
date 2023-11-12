from peewee import *
from models.BaseModel import *
# from datetime import time
import datetime


class Shift_time(BaseModel):
    name = CharField(max_length=50)
    shift_Type = CharField(max_length=50)
    entry_start_time = TextField()
    entry_end_time = TextField()
    delay_times = TextField()
    checkout_start_time = TextField()
    checkout_end_time = TextField()
    pay_per_shift = CharField(max_length=30)
    created_at = DateTimeField(default=datetime.datetime.now)
    updated_at = DateTimeField(default=datetime.datetime.now)

    def save(self, *args, **kwargs):
        self.updated_at = datetime.datetime.now()
        return super(Shift_time, self).save(*args, **kwargs)


db.create_tables([Shift_time, ])
