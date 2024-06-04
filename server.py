from flask import Flask, request, jsonify
import pytesseract
from PIL import Image
import logging
import os
import io

app = Flask(__name__)

# Set the Tesseract executable path if not in PATH
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Set the TESSDATA_PREFIX environment variable
os.environ['TESSDATA_PREFIX'] = r'C:\Program Files\Tesseract-OCR\tessdata'

@app.route('/')
def index():
    return "Welcome to the OCR API. Use /get-text and /get-bboxes endpoints to process images.", 200

@app.route('/get-text', methods=['POST'])
def get_text():
    try:
        if 'image' not in request.files:
            return jsonify({'error': 'No image file in request'}), 400
        image_file = request.files['image']
        image = Image.open(io.BytesIO(image_file.read()))
        text = pytesseract.image_to_string(image)
        return jsonify({'text': text})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/get-bboxes', methods=['POST'])
def get_bboxes():
    try:
        if 'image' not in request.files:
            return jsonify({'error': 'No image file in request'}), 400
        image_file = request.files['image']
        image = Image.open(io.BytesIO(image_file.read()))
        data = pytesseract.image_to_data(image, output_type=pytesseract.Output.DICT)
        return jsonify({'bboxes': data})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
