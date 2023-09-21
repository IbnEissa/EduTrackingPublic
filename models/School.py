from peewee import *
from models.BaseModel import BaseModel ,db
from models.City import City
import datetime
from models.Directorate import Directory


class School(BaseModel):
    school_name = CharField(max_length=100)
    city = ForeignKeyField(model=City, backref="schools")
    directorate = ForeignKeyField(model=Directory, backref="schools")
    village = CharField(max_length=30)
    academic_level = CharField(max_length=20)
    student_gender_type = CharField(max_length=10)
    created_at = DateTimeField(default=datetime.datetime.now)
    updated_at = DateTimeField()

    def save(self, *args, **kwargs):
        self.updated_at = datetime.datetime.now()
        return super(School, self).save(*args, **kwargs)


db.create_tables([School])
