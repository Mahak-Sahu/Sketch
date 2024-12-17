import os
import cv2
import numpy as np
from flask import Flask, request, jsonify, send_from_directory

app = Flask(__name__)

# Folder to store uploaded images
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Folder to store output images (sketches)
OUTPUT_FOLDER = 'static/sketches'
if not os.path.exists(OUTPUT_FOLDER):
    os.makedirs(OUTPUT_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER


# Function to convert image to pencil sketch
def convert_to_sketch(image_path):
    # Read the image
    image = cv2.imread(image_path)
    if image is None:
        return None

    # Apply grayscale filter
    grey_filter = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Invert the grayscale image
    invert = cv2.bitwise_not(grey_filter)

    # Apply Gaussian blur to the inverted image
    blur = cv2.GaussianBlur(invert, (51, 51), 0)

    # Invert the blurred image
    invertedblur = cv2.bitwise_not(blur)

    # Create the sketch effect
    sketch_filter = cv2.divide(grey_filter, invertedblur, scale=150.0)

    # Save the output image
    output_path = os.path.join(OUTPUT_FOLDER, 'output.png')
    cv2.imwrite(output_path, sketch_filter)
    return output_path


# Route to handle image upload and sketch conversion
@app.route('/convert', methods=['POST'])
def convert_image():
    if 'image' not in request.files:
        return jsonify({'success': False, 'message': 'No file part'}), 400

    file = request.files['image']

    if file.filename == '':
        return jsonify({'success': False, 'message': 'No selected file'}), 400

    # Save the uploaded file
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(file_path)

    # Convert image to pencil sketch
    sketch_path = convert_to_sketch(file_path)

    if sketch_path is None:
        return jsonify({'success': False, 'message': 'Failed to convert image'}), 500

    # Return the URL of the generated sketch
    return jsonify({'success': True, 'sketch_url': '/' + sketch_path})


# Serve static files
@app.route('/static/<path:filename>')
def serve_file(filename):
    return send_from_directory(OUTPUT_FOLDER, filename)


if __name__ == '__main__':
    app.run(debug=True)
