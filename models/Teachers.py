from peewee import *
from models.BaseModel import BaseModel, db
# from db import *
from models.Members import Members


class Teachers(BaseModel):
    members_id = ForeignKeyField(Members, backref='members')
    Shift_type = CharField()
    major = CharField()
    task = CharField()
    exceperiance_years = IntegerField()
    qualification = CharField()
    date_qualification = CharField()
    state = CharField()
    fingerPrintData = CharField()

    class Meta:
        table_name = 'teachers'

    def get_teacher_by_id(self, id):
        try:
            class_obj = Teachers.get(Teachers.id == id)
            return class_obj
        except DoesNotExist:
            return None


db.create_tables([Teachers])
