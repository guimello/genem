from flask import Flask, render_template, request, jsonify
from models import *

app = Flask(__name__, static_folder="public", static_url_path="")
connect("genemprod")

@app.route("/", methods=['GET'])
def home():
    return render_template("layout.html", title = "Test App")

@app.route("/find_school", methods=['GET'])
def find_school():
    school_name = request.args.get("term").upper()
    schools = School.objects(name__contains=school_name).order_by("name")

    json_dict = dict(schools = [])
    for s in schools:
        json_dict["schools"].append(dict(code=s.code, name=s.name))
    return jsonify(json_dict)

@app.route("/chart", methods=['GET'])
def chart():
    school_code = request.args.get("school")
    school = School.objects.get(code=school_code)
    city = City.objects.get(code=school.city_code)

    return jsonify(dict(
        school=dict(code=school.code, name=school.name, grades=school.grades, relative_grades=school.relative_grades()),
        city=dict(code=city.code, name=city.name, grades=city.grades, relative_grades=city.relative_grades())))

if __name__ == "__main__":
    app.run(port = 3000)
