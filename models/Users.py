import datetime
from peewee import *
from models.BaseModel import BaseModel, db
from models.Members import Members
from models.School import School


class Users(BaseModel):
    # school_id = ForeignKeyField(School, backref='school')
    account_type = CharField()
    Name = CharField()
    userName = CharField()
    userPassword = CharField()
    created_at = DateTimeField(default=datetime.datetime.now)
    updated_at = DateTimeField(default=datetime.datetime.now)
    state = CharField()
    initialization = CharField()

    class Meta:
        table_name = 'users'

    def save(self, *args, **kwargs):
        self.updated_at = datetime.datetime.now
        return super(Users, self).save(*args, **kwargs)

    @staticmethod
    def get_name_with_true_state():
        try:
            user = Users.select(Users.Name).where(Users.state == 'True').get()
            return user.Name
        except Users.DoesNotExist:
            return None

    @staticmethod
    def update_all_states_to_false():
        Users.update(state=False).execute()


# db.create_tables([Users])
