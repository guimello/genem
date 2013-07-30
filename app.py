from flask import Flask, render_template
from models import *

app = Flask(__name__, static_folder="public", static_url_path="")
connect("genem")

@app.route("/")
def home():
    return render_template("layout.html", title = "Test App")


if __name__ == "__main__":
    app.run(port = 3000)
