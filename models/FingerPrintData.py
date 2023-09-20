from datetime import datetime
from peewee import *
from models.BaseModel import BaseModel, db
from models.Teachers import Teachers


class FingerPrintData(BaseModel):
    teacherId = ForeignKeyField(Teachers, backref='teachers')
    f1 = CharField()
    f2 = CharField()

    class Meta:
        table_name = 'finger_print_data'


# db.create_tables([FingerPrintData])
