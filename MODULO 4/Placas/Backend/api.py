import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from ocr_engine import extract_plate_text
from models import find_owner_by_plate

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/", methods=["GET"])
def index():
    return jsonify({"status": "API activa", "message": "Sistema de detección de placas"}), 200

@app.route("/api/lookup_plate", methods=["POST"])
def lookup_plate():
    try:
        if "image" not in request.files:
            return jsonify({"error": "No se envió ninguna imagen."}), 400

        file = request.files["image"]
        if file.filename == "":
            return jsonify({"error": "Archivo vacío."}), 400

        image_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(image_path)

        plate_text, confidence = extract_plate_text(image_path)

        if not plate_text:
            return jsonify({
                "error": "No se detectó ninguna placa.",
                "ocr_confidence": confidence
            }), 404

        owner = find_owner_by_plate(plate_text)

        return jsonify({
            "plate": plate_text,
            "ocr_confidence": confidence,
            "owner": owner
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
