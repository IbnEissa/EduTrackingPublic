from datetime import datetime
from peewee import *
from models.BaseModel import BaseModel, db
# from db import *
# from db import BaseModel
from models.School import School


class Members(BaseModel):
    school_id = ForeignKeyField(School, backref='school')
    fName = CharField()
    lName = CharField()
    dateBerth = CharField()
    phone = IntegerField()

    class Meta:
        table_name = 'members'

    def get_members_by_id(self, id):
        try:
            class_obj = Members.get(Members.id == id)
            return class_obj
        except DoesNotExist:
            return None

    def get_member_id_from_name(self, member_name):
        try:
            member_object = Members.get(Members.name == member_name)
            return member_object.id
        except DoesNotExist:
            return None


db.create_tables([Members])
