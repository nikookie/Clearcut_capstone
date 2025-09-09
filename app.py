from flask import Flask, request, render_template, jsonify
from werkzeug.utils import secure_filename
import os
from ultralytics import YOLO

app = Flask(__name__)

# Configure upload folder
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Load YOLO model
model = YOLO("best.pt")  # replace with your model

# ---------------------------
# Route: JSON API (For Flutter)
# ---------------------------
@app.route('/predict', methods=['POST'])
def predict():
    if 'image' not in request.files:
        return jsonify({"error": "No image uploaded"}), 400

    file = request.files['image']
    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)

    results = model.predict(source=filepath, save=False)

    if results and len(results[0].boxes) > 0:
        box = results[0].boxes[0]
        label = model.names[int(box.cls[0])]
        confidence = round(float(box.conf[0]) * 100, 2)  # % confidence

        # Example suggested uses per wood type
        suggestions = {
            "mahogany": "Furniture, cabinets, doors",
            "oak": "Flooring, tables, chairs",
            "narra": "Premium furniture, carvings",
        }
        suggested_use = suggestions.get(label.lower(), "General purpose")

        return jsonify({
            "wood_type": label,
            "confidence": confidence,     # send percentage
            "suggested_use": suggested_use
        })
    else:
        return jsonify({
            "wood_type": None,
            "confidence": 0,
            "suggested_use": "No wood detected"
        })

if __name__ == '__main__':
    app.run(debug=True)
