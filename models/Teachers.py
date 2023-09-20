from peewee import *
from models.BaseModel import BaseModel, db
from models.Members import Members


class Teachers(BaseModel):
    members_id = ForeignKeyField(Members, backref='members')
    major = CharField()
    task = CharField()
    state = CharField()
    fingerPrintData = CharField()

    class Meta:
        table_name = 'teachers'


# db.create_tables([Teachers])
