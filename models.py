from mongoengine import *

class PercentageGrade(object):
    def relative_grades(self):
        total = float(sum(self.grades))
        return [ g / total * 100 for g in self.grades ]

class State(Document, PercentageGrade):
    code = StringField(required = True)
    grades = ListField(IntField())

    def to_json(self):
        return dict(
                code=self.code,
                grades=self.grades,
                relative_grades=self.relative_grades())

class City(Document, PercentageGrade):
    code = IntField(required = True)
    name = StringField(required = True)
    state_code = StringField(required = True)
    grades = ListField(IntField())

    def to_json(self):
        return dict(
                code=self.code,
                name=self.name,
                state_code=self.state_code,
                grades=self.grades,
                relative_grades=self.relative_grades())

class School(Document, PercentageGrade):
    code = IntField(required = True)
    name = StringField(required = True)
    city_code = IntField(required = True)
    state_code = StringField(required = True)
    grades = ListField(IntField())

    def to_json(self):
        return dict(
                code=self.code,
                name=self.name,
                city_code=self.city_code,
                state_code=self.state_code,
                grades=self.grades,
                relative_grades=self.relative_grades())
