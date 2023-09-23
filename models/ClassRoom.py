from peewee import *
from models.BaseModel import BaseModel, db
from models.School import School
from models.Teachers import Teachers


class ClassRoom(BaseModel):
    school_id = ForeignKeyField(model=School, backref="Users")
    name = CharField(max_length=20, unique=True)

    @classmethod
    def add(cls, school_id, names):
        created_classes = []
        for name in names:
            class_obj = cls(
                school_id=school_id,
                name=name,
            )
            class_obj.save()
            created_classes.append(class_obj)
        return created_classes

# db.create_tables([ClassRoom])
