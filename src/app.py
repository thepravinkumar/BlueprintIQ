from flask import Flask, request, jsonify, render_template
import os
import ezdxf
import random

app = Flask(__name__)

# Engineering mottos
mottos = [
    "Precision is the key to great engineering.",
    "A strong foundation leads to a strong structure.",
    "Measure twice, cut once.",
    "Every structure tells a story of its engineer.",
    "Engineering is about doing, not just knowing.",
    "Accuracy builds trust in construction.",
    "Bridges connect places, engineers connect ideas."
]

def get_unique_motto():
    return random.choice(mottos)

def analyze_dxf(file_path):
    """Processes the DXF file and extracts dimensions."""
    doc = ezdxf.readfile(file_path)
    msp = doc.modelspace()
    
    entities = [e for e in msp.query('LINE POLYLINE LWPOLYLINE')]
    if not entities:
        return {"error": "No valid entities found in the DXF file."}

    x_coords, y_coords = [], []
    for entity in entities:
        if entity.dxftype() == 'LINE':
            x_coords.extend([entity.dxf.start.x, entity.dxf.end.x])
            y_coords.extend([entity.dxf.start.y, entity.dxf.end.y])
        elif entity.dxftype() in ['LWPOLYLINE', 'POLYLINE']:
            points = [(p[0], p[1]) for p in entity.get_points()]
            x_coords.extend([p[0] for p in points])
            y_coords.extend([p[1] for p in points])

    # Compute dimensions
    min_x, max_x = min(x_coords), max(x_coords)
    min_y, max_y = min(y_coords), max(y_coords)

    internal_length = max_x - min_x
    internal_breadth = max_y - min_y
    external_length = internal_length * 1.02
    external_breadth = internal_breadth * 1.02

    w = external_length - internal_length
    k = external_breadth - internal_breadth
    perimeter = 2 * ((internal_length + w / 2) + (internal_breadth + k / 2))

    return {
        "internal_length": round(internal_length, 2),
        "external_length": round(external_length, 2),
        "internal_breadth": round(internal_breadth, 2),
        "external_breadth": round(external_breadth, 2),
        "perimeter": round(perimeter, 2),
        "motto": get_unique_motto()
    }

@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Welcome to DXF Analyzer API!"})

@app.route("/analyze", methods=["POST"])
def analyze():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    file_path = os.path.join("uploads", file.filename)
    os.makedirs("uploads", exist_ok=True)
    file.save(file_path)

    result = analyze_dxf(file_path)
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)
