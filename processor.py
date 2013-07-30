from parsers import *
from models import *
import traceback

class Processor(object):
    def __init__(self, enem_file_name, city_names_file_name):
        self.enem_file_name = enem_file_name
        self.school_parser = SchoolParser(file_name = city_names_file_name)

    def work(self):
        with open(self.enem_file_name) as f:
            for line in f:
                try:
                    enem_parser = EnemParser(data = line)
                    if not enem_parser.has_attended(): continue

                    school = self._parse_school(enem_parser)
                    city = self._parse_city(enem_parser, school)
                    state = self._parse_state(enem_parser, city)
                except StopIteration as si:
                    pass
                except Exception as e:
                    traceback.print_exc()

    def _parse_school(self, enem_parser):
        school = School.objects(code = enem_parser.school_code()).first()

        if not school:
            school = School(
                    code = enem_parser.school_code(),
                    name = self.school_parser.school_name(enem_parser.school_code()),
                    city_code = enem_parser.city_code(),
                    state_code = enem_parser.state_code())

        school.grades = self._compute_grade(student_grade = enem_parser.grade(), db_grade = school.grades)
        school.save()
        return school

    def _parse_city(self, enem_parser, school):
        city = City.objects(code = school.city_code).first()

        if not city:
            city = City(
                    code = school.city_code,
                    name = enem_parser.city_name(),
                    state_code = school.state_code)

        city.grades = self._compute_grade(student_grade = enem_parser.grade(), db_grade = city.grades)
        city.save()
        return city

    def _parse_state(self, enem_parser, city):
        state = State.objects(code = city.state_code).first()

        if not state:
            state = State(code = city.state_code)

        state.grades = self._compute_grade(student_grade = enem_parser.grade(), db_grade = state.grades)
        state.save()
        return state

    def _compute_grade(self, student_grade, db_grade):
        db_grade = db_grade or self._default_grade()
        bucket = self._grade_bucket(student_grade)
        db_grade[bucket] = db_grade[bucket] + 1

        return db_grade

    def _default_grade(self):
        return [0 for _ in xrange(10)]

    def _grade_bucket(self, grade):
        if grade >= 0 and grade <= 99.99:
            return 0
        elif grade >= 100 and grade <= 199.99:
            return 1
        elif grade >= 200 and grade <= 299.99:
            return 2
        elif grade >= 300 and grade <= 399.99:
            return 3
        elif grade >= 400 and grade <= 499.99:
            return 4
        elif grade >= 500 and grade <= 599.99:
            return 5
        elif grade >= 600 and grade <= 699.99:
            return 6
        elif grade >= 700 and grade <= 799.99:
            return 7
        elif grade >= 800 and grade <= 899.99:
            return 8
        elif grade >= 900 and grade <= 1000:
            return 9
