from parsers import *
from models import *
from processor import *

connect("genemprod")


# TODO: find a way to clean the db, not doing this
def clean_up_db():
    for m in [State, City, School]:
        m.drop_collection()

clean_up_db()
print "Started"

processor = Processor(enem_file_name = "./enem_cidade_sao_paulo.txt", city_names_file_name = "./escolas_cidade_sao_paulo.csv")
processor.work()

print "Total not found: %i" % len(processor.school_parser.not_found_codes)
with open("./not_found.txt", "w") as f:
    for i in processor.school_parser.not_found_codes:
        f.write(i + "\n")

print "Done"
