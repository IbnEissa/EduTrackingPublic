from datetime import datetime
from peewee import *
from models.BaseModel import BaseModel, db

STUDENT_GENDER_TYPE = (
    ('طلاب', 'طلاب'),
    ('طالبات', 'طالبات'),
    ('مختلط', 'مختلط'),

)
ACADEMIC_LEVEL = (
    ('أبتدائي', 'أبتدائي'),
    ('عدادي', 'عدادي'),
    ('ثانوب', 'ثانوب'),
    ('أساسي', 'أساسي'),
    ('شامل', 'شامل'),

)


class School(BaseModel):
    schoolName = CharField()
    city= CharField()
    directorate= CharField()
    village = CharField()
    academicLevel = CharField(choices=ACADEMIC_LEVEL)
    studentsGenderType = CharField(choices=STUDENT_GENDER_TYPE)

    class Meta:
        table_name = 'School'


# db.create_tables([School])
