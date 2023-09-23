from peewee import *
from models.BaseModel import BaseModel, db


class Subjects(BaseModel):
    name = CharField(max_length=70)

    @classmethod
    def add(cls, names):
        created_subjects = []
        for name in names:
            subject_obj = cls(
                name=name,
            )
            subject_obj.save()
            created_subjects.append(subject_obj)
        return created_subjects

# db.create_tables([Subjects])
