from mongoengine import *

class PercentageGrade(object):
    def relative_grades(self):
        total = float(sum(self.grades))
        return [ g / total * 100 for g in self.grades ]

class State(Document, PercentageGrade):
    code = StringField(required = True)
    grades = ListField(IntField())

class City(Document, PercentageGrade):
    code = IntField(required = True)
    name = StringField(required = True)
    state_code = StringField(required = True)
    grades = ListField(IntField())

class School(Document, PercentageGrade):
    code = IntField(required = True)
    name = StringField(required = True)
    city_code = IntField(required = True)
    state_code = StringField(required = True)
    grades = ListField(IntField())
