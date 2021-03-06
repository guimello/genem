from parsers import *
from models import *
import traceback
import logging

class Processor(object):
    """Loads the ENEM file parsing and saving to the db"""

    def __init__(self, enem_file_name, city_names_file_name):
        self.enem_file_name = enem_file_name
        self.school_parser = SchoolParser(file_name = city_names_file_name)

    def work(self):
        """Starts the load process"""
        with open(self.enem_file_name) as f:
            for line in f:
                try:
                    enem_parser = EnemParser(data = line)
                    # if user has not attended the specific test, discard
                    if not enem_parser.has_attended(): continue

                    school = self._parse_school(enem_parser)
                    city = self._parse_city(enem_parser, school)
                    state = self._parse_state(enem_parser, city)
                except StopIteration as si:
                    pass
                except Exception as e:
                    logging.info(traceback.print_exc() or e)

    def _parse_school(self, enem_parser):
        """Parses and save/update a school"""
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
        """Parses and save/update a city"""
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
        """Parses and save/update a state"""
        state = State.objects(code = city.state_code).first()

        if not state:
            state = State(code = city.state_code)

        state.grades = self._compute_grade(student_grade = enem_parser.grade(), db_grade = state.grades)
        state.save()
        return state

    def _compute_grade(self, student_grade, db_grade):
        """Computes the grade increasing the amount of students that had the same grade class (range)"""
        db_grade = db_grade or self._default_grade()
        bucket = self._grade_bucket(student_grade)
        db_grade[bucket] = db_grade[bucket] + 1

        return db_grade

    def _default_grade(self):
        """Initial grade"""
        return [0 for _ in xrange(10)]

    def _grade_bucket(self, grade):
        """Find the index that the grade will be incresed to"""
        return int(grade / 100)
