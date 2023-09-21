from peewee import Model, MySQLDatabase

db = MySQLDatabase('EduTrackingSystemDB2', user='root', password='',
                   host='localhost')


class BaseModel(Model):
    class Meta:
        database = db


