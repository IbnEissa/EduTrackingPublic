from datetime import datetime
from peewee import *
from models.BaseModel import BaseModel, db
# from db import *
# from db import BaseModel
from models.School import School


class Members(BaseModel):
    school_id = ForeignKeyField(School, backref='school')
    fName = CharField()
    sName = CharField()
    tName = CharField()
    lName = CharField()
    phone = IntegerField()
    dateBerth = CharField()

    class Meta:
        table_name = 'members'


# db.create_tables([Members])
