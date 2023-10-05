from peewee import *
from models.BaseModel import BaseModel, db
from models.ClassRoom import ClassRoom
from models.Members import Members


class TeacherSubjectClassRoomTermTable(BaseModel):
    teacher_id = ForeignKeyField(model=Members, backref='Teacher_Subjects')
    subject_id = CharField()
    class_room_id = ForeignKeyField(model=ClassRoom, backref='Teacher_Subjects')
    number_of_lessons = IntegerField()

    term_id = None

    def get_elements(self, term_id, class_name, subject, number_of_sessions):
        return term_id, class_name, subject, number_of_sessions

# db.create_tables([TeacherSubjectClassRoomTermTable])
