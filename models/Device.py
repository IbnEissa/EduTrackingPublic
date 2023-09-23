from peewee import *
from models.BaseModel import BaseModel, db
from models.School import School


class Device(BaseModel):
    school_id = ForeignKeyField(model=School, backref='Devices')
    name = CharField(max_length=30)
    ip = CharField(max_length=20)
    port = IntegerField()
    status = CharField(max_length=20)

    @classmethod
    def add(cls, school_id, name, ip, port, status):
        device = cls(
            school_id=school_id,
            name=name,
            ip=ip,
            port=port,
            status=status,
        )
        device.save()
        return device

# db.create_tables([Device])
