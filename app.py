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
    schools = School.objects(name__contains = school_name).order_by("name")

    json_dict = dict(schools = [])
    for s in schools:
        json_dict["schools"].append(dict(code=s.code, name=s.name))
    return jsonify(json_dict)


if __name__ == "__main__":
    app.run(port = 3000)
