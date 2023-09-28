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

    def get_class_id_from_name(self, class_name):
        try:
            class_obj = ClassRoom.get(ClassRoom.name == class_name)
            return class_obj.id
        except DoesNotExist:
            return None

    def get_class_name_from_id(self, class_id):
        try:
            class_obj = ClassRoom.get(ClassRoom.id == class_id)
            return class_obj.name
        except DoesNotExist:
            return None

    # this is the method that update the data in the database with data that takes as a parameters


# db.create_tables([ClassRoom])
