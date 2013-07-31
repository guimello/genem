import unittest
from parsers import *
from models import *
from processor import *

connect("genemtest")

# TODO: find a way to clean the db, not doing this
def clean_up_db():
    for m in [State, City, School]:
        m.drop_collection()

# Fixture data used to compare to the parsed data
fixture_data = dict(
        school_code = 35058836,
        school_name = "LEANDRO FRANCESCHINI DR ESCOLA MUNICIPAL",
        city_code = 3552403,
        city_name = "SUMARE",
        state_code = "SP",
        grade = 543.30,
        grade_frequency = [0, 0, 0, 0, 0, 1, 0, 0, 0, 0])

class EnemParserTest(unittest.TestCase):
    def setUp(self):
        with open("./fixtures/enem.txt") as f:
            line = f.readline()
        self.parser = EnemParser(data = line)

    def test_parse_school_code(self):
        self.assertEqual(self.parser.school_code(), fixture_data["school_code"])

    def test_parse_city_code(self):
        self.assertEqual(self.parser.city_code(), fixture_data["city_code"])

    def test_parse_city_name(self):
        self.assertEqual(self.parser.city_name(), fixture_data["city_name"])

    def test_parse_state_code(self):
        self.assertEqual(self.parser.state_code(), fixture_data["state_code"])

    def test_parse_has_attended(self):
        self.assertTrue(self.parser.has_attended())

    def test_parse_grade(self):
        self.assertEqual(self.parser.grade(), fixture_data["grade"])


class SchoolParserTest(unittest.TestCase):
    def setUp(self):
        self.parser = SchoolParser(file_name = "./fixtures/city_names.csv")

    def test_parse_school_name(self):
        self.assertEqual(self.parser.school_name(fixture_data["school_code"]), fixture_data["school_name"])


class ProcessorTest(unittest.TestCase):
    def setUp(self):
        clean_up_db()
        self.processor = Processor(enem_file_name = "./fixtures/enem.txt", city_names_file_name = "./fixtures/city_names.csv")
        self.processor.work()

    def test_create_a_state(self):
        state = State.objects.first()
        self.assertEqual(state.code, fixture_data["state_code"])
        self.assertEqual(state.grades, fixture_data["grade_frequency"])

    def test_create_a_city(self):
        city = City.objects.first()
        self.assertEqual(city.code, fixture_data["city_code"])
        self.assertEqual(city.name, fixture_data["city_name"])
        self.assertEqual(city.state_code, fixture_data["state_code"])
        self.assertEqual(city.grades, fixture_data["grade_frequency"])

    def test_create_a_school(self):
        school = School.objects.first()
        self.assertEqual(school.code, fixture_data["school_code"])
        self.assertEqual(school.name, fixture_data["school_name"])
        self.assertEqual(school.city_code, fixture_data["city_code"])
        self.assertEqual(school.state_code, fixture_data["state_code"])
        self.assertEqual(school.grades, fixture_data["grade_frequency"])

    def test_updates_a_state(self):
        self.processor.work() # Redo work to fake data
        state = State.objects.first()
        self.assertEqual(state.grades, [0, 0, 0, 0, 0, 2, 0, 0, 0, 0])

    def test_updates_a_city(self):
        self.processor.work() # Redo work to fake data
        city = City.objects.first()
        self.assertEqual(city.grades, [0, 0, 0, 0, 0, 2, 0, 0, 0, 0])

    def test_updates_a_school(self):
        self.processor.work() # Redo work to fake data
        school = School.objects.first()
        self.assertEqual(school.grades, [0, 0, 0, 0, 0, 2, 0, 0, 0, 0])

    def test_grade_bucket(self):
        self.assertEqual(self.processor._grade_bucket(33.45), 0)
        self.assertEqual(self.processor._grade_bucket(450.0), 4)


if __name__ == "__main__":
    unittest.main()
