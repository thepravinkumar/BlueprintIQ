from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    return "BlueprintIQ is running!"

@app.route("/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    file = request.files["file"]
    return jsonify({"message": f"Received {file.filename}"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
