from mongoengine import *

class State(Document):
    code = StringField(required = True)
    grades = ListField(IntField())

class City(Document):
    code = IntField(required = True)
    name = StringField(required = True)
    state_code = StringField(required = True)
    grades = ListField(IntField())

class School(Document):
    code = IntField(required = True)
    name = StringField(required = True)
    city_code = IntField(required = True)
    state_code = StringField(required = True)
    grades = ListField(IntField())
