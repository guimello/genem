class EnemParser(object):
    def __init__(self, data):
        self.data = data

    def school_code(self):
        return int(self.data[204-1:204-1+8].strip())

    def city_code(self):
        return int(self.data[212-1:212-1+7].strip())

    def city_name(self):
        return self.data[219-1:219-1+150].strip()

    def state_code(self):
        return self.data[369-1:369-1+2].strip()

    def has_attended(self):
        """Returns whether or not the student attended the test"""
        return self.data[533-1:533-1+1] == '1'

    def grade(self):
        return float(self.data[537-1:537-1+9].strip())


class SchoolParser(object):
    def __init__(self, file_name):
        self.file_name = file_name
        self.not_found_codes = set()

    def school_name(self, code):
        """Returns the city name based on its code"""
        return self.__line_for_city_code(code).split(",")[3].strip()

    def __line_for_city_code(self, code):
        """Parses one line given a city code"""
        code = str(code)
        try:
            return next(line for line in open(self.file_name) if line.split(",")[2] == code)
        except StopIteration:
            self.not_found_codes.add(code)
            print "Could not find city name with code %s" % code
            raise
