from flask import Flask, request, jsonify, render_template
from flask_cors import CORS

app = Flask(__name__)
# Allow requests from your Vercel frontend
CORS(app) 

# Counter dictionary
counter = {"cracked": 0, "uncracked": 0, "total": 0}

@app.route("/")
def home():
    return "Egg Counter Backend is running!"

@app.route("/record", methods=["POST"])
def record():
    """Records a cracked (0) or uncracked (1) egg."""
    data = request.get_json()
    value = data.get("value")

    if value == 0:
        counter["cracked"] += 1
    elif value == 1:
        counter["uncracked"] += 1
    
    counter["total"] = counter["cracked"] + counter["uncracked"]
    return jsonify(counter)

@app.route("/reduce", methods=["POST"])
def reduce_count():
    """Reduces the count for cracked (0) or uncracked (1) eggs."""
    data = request.get_json()
    value = data.get("value")

    if value == 0 and counter["cracked"] > 0:
        counter["cracked"] -= 1
    elif value == 1 and counter["uncracked"] > 0:
        counter["uncracked"] -= 1
        
    counter["total"] = counter["cracked"] + counter["uncracked"]
    return jsonify(counter)


@app.route("/get_count", methods=["GET"])
def get_count():
    """Returns the current counts."""
    return jsonify(counter)

@app.route("/reset", methods=["POST"])
def reset():
    """Resets all counters to zero."""
    global counter
    counter = {"cracked": 0, "uncracked": 0, "total": 0}
    return jsonify({"message": "Counters reset successfully!", "counter": counter})

# This part is for local testing. Render will use its own command to run the app.
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8001)
