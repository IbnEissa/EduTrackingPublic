from peewee import *
from db import *
from Teachers import Teachers


class FingerPrintData(BaseModel):
    teacher_id = ForeignKeyField(model=Teachers, backref='Finger_Print_Datas')
    finger_id = IntegerField()
    device_number = IntegerField()
    card_id = IntegerField()
    password = CharField(max_length=30)
    f1 = IntegerField()
    f2 = IntegerField()


db.create_tables([FingerPrintData])
