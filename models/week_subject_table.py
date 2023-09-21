from peewee import *
from db import *
from Subjects import Subjects
# from teacher import Teacher
from ClassRoom import ClassRoom
from Members import Members
from Users import Users


class TeacherSubjectClassRoom(BaseModel):
    teacher_id = ForeignKeyField(model=Members, backref='Teacher_Subjects')
    subject_id = ForeignKeyField(model=Subjects, backref='Teacher_Subjects')
    class_room_id = ForeignKeyField(model=ClassRoom, backref='Teacher_Subjects')
    number_of_lessons = IntegerField()

    # class Meta:
    #     primary_key = CompositeKey('teacher_id', 'subjeci_id', 'class_room_id')


db.create_tables([TeacherSubjectClassRoom])
