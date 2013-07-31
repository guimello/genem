from parsers import *
from models import *
from processor import *
import logging

connect("genemprod")

# TODO: find a way to clean the db, not doing this
def clean_up_db():
    for m in [State, City, School]:
        m.drop_collection()

clean_up_db()

# Setup logging
logging.basicConfig(filename='./log/parser.log', level=logging.INFO, format='[%(asctime)s] %(message)s')
logging.info("===Started===")

processor = Processor(enem_file_name = "./inep/enem_cidade_sao_paulo.txt", city_names_file_name = "./inep/escolas_cidade_sao_paulo.csv")
processor.work()

logging.info("Total not found: %i" % len(processor.school_parser.not_found_codes))

# Print all not found city codes (could not find the school's name)
for code in processor.school_parser.not_found_codes:
    logging.info(code)

logging.info("===Done===")
