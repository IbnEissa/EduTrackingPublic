from datetime import datetime
from peewee import *
from models.BaseModel import BaseModel, db
# from db import *
# from db import BaseModel
from models.School import School


class Teachers_Schedule(BaseModel):
    Teacher_Name = CharField()
    Day = CharField()
    Subject = CharField()
    session = CharField()
    Class_Name = CharField()

    class Meta:
        table_name = 'teachers_schedule'

# db.create_tables([Teachers_Schedule])
