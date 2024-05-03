from flask import Flask, render_template, request, send_file
import cv2
import numpy as np
from io import BytesIO

app = Flask(__name__)

def find_edges(image):
    # Convert image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Find edges using Canny edge detection
    edges = cv2.Canny(gray, 100, 200)
    return edges

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return "No file part"
    
    file = request.files['file']
    if file.filename == '':
        return "No selected file"
    
    # Read the uploaded file
    nparr = np.frombuffer(file.read(), np.uint8)
    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    # Find edges
    edges = find_edges(image)

    # Convert edges image to bytes
    _, buffer = cv2.imencode('.jpg', edges)
    edge_bytes = BytesIO(buffer)

    return send_file(edge_bytes, mimetype='image/jpeg')

if __name__ == '__main__':
    app.run(debug=True)
