from flask import Flask, request, jsonify, render_template
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

counter = {"zero": 0, "one": 0, "total": 0}

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/record", methods=["POST"])
def record():
    data = request.get_json()


    if data["value"] == 0:
        counter["zero"] += 1
    elif data["value"] == 1:
        counter["one"] += 1
    counter["total"] += 1

    return jsonify(counter)

@app.route("/get_count")
def get_count():
    return jsonify(counter)

@app.route("/reset", methods=["POST"])
def reset():
    global counter
    counter = {"zero": 0, "one": 0, "total": 0}
    return jsonify(counter)     
if __name__ == "__main__":
    app.run(port=8001)  # Now use http://localhost:8001
