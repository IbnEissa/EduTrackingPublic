from peewee import *
from models.BaseModel import BaseModel
from models.City import Cities
import datetime
from models.Directorate import Directories


class School(BaseModel):
    school_name = CharField(max_length=100)
    city = ForeignKeyField(Cities, backref="schools")
    directorate = ForeignKeyField(Directories, backref="schools")
    village = CharField(max_length=30)
    academic_level = CharField(max_length=20)
    student_gender_type = CharField(max_length=10)
    created_at = DateTimeField(default=datetime.datetime.now)
    updated_at = DateTimeField()

    def save(self, *args, **kwargs):
        self.updated_at = datetime.datetime.now()
        return super().save(*args, **kwargs)

    @classmethod
    def add(cls, name, city, directorate, village, academic_level, student_gender_type):
        school = cls(
            school_name=name,
            city=city,
            directorate=directorate,
            village=village,
            academic_level=academic_level,
            student_gender_type=student_gender_type
        )
        school.save()
        return school
        # db.create_tables([School])
