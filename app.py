import os
import uuid
from flask import Flask, request, jsonify, send_from_directory, send_file
from werkzeug.utils import secure_filename
import cv2
import numpy as np

app = Flask(__name__, static_folder='build', static_url_path='')
UPLOAD_FOLDER = "uploads"
RESULT_FOLDER = "results"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULT_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['RESULT_FOLDER'] = RESULT_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def enhance_image(image):
    lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)
    l = cv2.equalizeHist(l)
    enhanced_image = cv2.merge([l, a, b])
    return cv2.cvtColor(enhanced_image, cv2.COLOR_LAB2BGR)

def detect_objects(image):
    # Placeholder for a real object detection model
    return [{"label": "Window", "confidence": 0.95}, {"label": "Door", "confidence": 0.90}, {"label": "Beam", "confidence": 0.85}]

def analyze_structure(image_path):
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError("Image not found.")
    image = enhance_image(image)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 50, 150)
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    result = image.copy()
    bounding_boxes = []
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        bounding_boxes.append({'x': x, 'y': y, 'width': w, 'height': h})
        cv2.rectangle(result, (x, y), (x + w, y + h), (255, 0, 0), 2)
    output_filename = f"{uuid.uuid4().hex}.png"
    output_path = os.path.join(RESULT_FOLDER, output_filename)
    cv2.imwrite(output_path, result)
    objects_detected = detect_objects(image)
    return output_filename, len(contours), bounding_boxes, objects_detected

@app.route('/upload', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    if not allowed_file(file.filename):
        return jsonify({"error": "File type not allowed"}), 400
    filename = secure_filename(file.filename)
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(file_path)
    try:
        output_filename, parts_count, bounding_boxes, objects_detected = analyze_structure(file_path)
        return jsonify({
            "message": "Analysis complete",
            "output_image": output_filename,
            "number_of_parts": parts_count,
            "bounding_boxes": bounding_boxes,
            "detected_objects": objects_detected
        })
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@app.route('/results/<filename>')
def get_result_image(filename):
    return send_from_directory(RESULT_FOLDER, filename)

# Serve React App
@app.route('/')
def serve():
    return send_file(os.path.join(app.static_folder, 'index.html'))

if __name__ == "__main__":
    app.run(debug=True)
