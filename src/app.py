from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/api/analyze', methods=['POST'])
def analyze():
    file = request.files.get('file')
    if not file:
        return jsonify({"error": "No file uploaded"}), 400
    
    # DXF file processing logic here
    return jsonify({"message": "File processed successfully"})

if __name__ == "__main__":
    app.run()
