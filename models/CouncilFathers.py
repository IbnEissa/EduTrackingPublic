from peewee import *
from models.BaseModel import BaseModel, db
from models.Members import Members


class CouncilFathers(BaseModel):
    members_id = ForeignKeyField(Members, backref='members')
    CouncilFathersTask = CharField()

    class Meta:
        table_name = 'CouncilFathers'


# db.create_tables([CouncilFathers])
