from flask import Flask, request, jsonify, render_template
from flask_cors import CORS

app = Flask(__name__)
# This is crucial! It allows your Vercel site to make requests to your backend.
CORS(app) 

# In-memory "database" for the counter
counter = {"zero": 0, "one": 0, "total": 0}

# This route is optional for an API, but good for testing if the server is up.
@app.route("/")
def home():
    # Note: render_template won't be used by your Vercel site.
    # Vercel handles serving index.html. This is just for direct access.
    return "Flask counter backend is running!"

@app.route("/record", methods=["POST"])
def record():
    data = request.get_json()
    if data.get("value") == 0:
        counter["zero"] += 1
    elif data.get("value") == 1:
        counter["one"] += 1
    counter["total"] = counter["zero"] + counter["one"]
    return jsonify(counter)

@app.route("/get_count", methods=["GET"])
def get_count():
    return jsonify(counter)

@app.route("/reset", methods=["POST"])
def reset():
    global counter
    counter = {"zero": 0, "one": 0, "total": 0}
    return jsonify({"message": "Counters reset successfully!", "counter": counter})

# The following is for local testing only. A real server will run the 'app' object.
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8001)
