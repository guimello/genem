import os
from flask import Flask, render_template, request, jsonify
from models import *

app = Flask(__name__, static_folder="public", static_url_path="")

# Db config
connection_opts = dict()
if os.environ.get('MONGOHQ_URL'): connection_opts['host'] = os.environ.get('MONGOHQ_URL')
connect("genemprod", **connection_opts)

@app.route("/", methods=['GET'])
def home():
    return render_template("home.html", title = "ENEM")

@app.route("/find_school", methods=['GET'])
def find_school():
    school_name = request.args.get("term").upper()
    schools = School.objects(name__contains=school_name).order_by("name")

    json_dict = dict(schools=[dict(code=s.code, name=s.name) for s in schools])
    return jsonify(json_dict)

@app.route("/chart/<int:school_code>", methods=['GET'])
def chart(school_code):
    school = School.objects.get(code=school_code)
    city = City.objects.get(code=school.city_code)

    return jsonify(dict(school=school.to_json(), city=city.to_json()))

if __name__ == "__main__":
    app.run(port = 3000)
