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

    def get_members_by_id(self, id):
        try:
            class_obj = Members.get(Members.id == id)
            return class_obj
        except DoesNotExist:
            return None
# db.create_tables([Members])
