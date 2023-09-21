from peewee import *
from db import *
from Members import Members
import datetime


class BoardFathers(BaseModel):
    member_id = ForeignKeyField(model=Members, backref="member", primary_key=True)
    social_status = CharField(max_length=20)
    address = CharField(max_length=50)
    organic_status = CharField()
    # created_at = DateTimeField(default=datetime.datetime.now)
    # updated_at = DateTimeField()

    # def save(self, *args, **kwargs):
    #     self.updated_at = datetime.datetime.now()
    #     return super(Board_fathers, self).save(*args, **kwargs)


db.create_tables([BoardFathers])
