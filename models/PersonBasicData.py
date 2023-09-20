# from datetime import datetime
#
# from peewee import *
#
# from models.BaseModel import BaseModel, db
#
# BLOOD_TYPE = (
#     ('O+', 'O موجب'),
#     ('O-', 'O سالب'),
#     ('A+', 'A موجب'),
#     ('A-', 'A سالب'),
#     ('B+', 'B موجب'),
#     ('B-', 'B سالب'),
#     ('AB+', 'AB موجب'),
#     ('AB-', 'AB سالب'),
# )
# MARITAL_STATUS = (
#     ('1', 'عازب'),
#     ('2', 'متزوج'),
#     ('3', 'أرمل'),
# )
# PROPIRTY_STATUS = (
#     ('1', 'ملك'),
#     ('2', 'إيجار'),
# )
# INCOME_STATUS = (
#     ('1', 'جيد'),
#     ('2', 'متوسط'),
#     ('3', 'ضعيف'),
# )
#
#
# class PersonBasicData(BaseModel):
#     firstName = CharField()
#     secondName = CharField()
#     thirdName = CharField()
#     fourthName = CharField()
#     fivthName = CharField()
#     lastName = CharField()
#     nickName = CharField()
#     phoneNumber = BigIntegerField()
#     dateOfBirth = CharField()
#     age = IntegerField(datetime.now() - dateOfBirth)
#     bloodType = CharField(choices=BLOOD_TYPE)
#     maritalStatus = CharField(choices=MARITAL_STATUS)
#     incomeStatus = CharField(choices=INCOME_STATUS)
#     propirtyStatus = CharField(choices=PROPIRTY_STATUS)
#     headMan = CharField()
#     nameOfSender = CharField()
#     directSupervisor = CharField()
#     genralSupervisor = CharField()
#     dateOfEnrollment = CharField()
#     ciOfBirth = CharField()
#     dirOfBirth = CharField()
#     vilOfBirth = CharField()
#     ciOfLiving = CharField()
#     dirOfLiving = CharField()
#     vilOfLiving = CharField()
#
#     class Meta:
#         table_name = 'personbasicdata'
#
#
# db.create_tables([PersonBasicData])
