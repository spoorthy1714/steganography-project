from flask import Flask, render_template, request
import cv2
import numpy as np
from encryption import encode_message
from decryption import decode_message

app = Flask(_name_)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/encode', methods=['POST'])
def encode():
    if 'image' not in request.files or 'message' not in request.form:
        return "No file or message provided", 400

    image_file = request.files['image']
    secret_message = request.form['message']

    image = cv2.imdecode(np.frombuffer(image_file.read(), np.uint8), cv2.IMREAD_COLOR)
    stego_image = encode_message(image, secret_message)

    cv2.imwrite('static/stego_image.png', stego_image)
    return "Message encoded successfully! Check static/stego_image.png"

@app.route('/decode', methods=['POST'])
def decode():
    if 'image' not in request.files:
        return "No file provided", 400

    image_file = request.files['image']
    image = cv2.imdecode(np.frombuffer(image_file.read(), np.uint8), cv2.IMREAD_COLOR)

    decoded_message = decode_message(image)
    return f"Decoded message: {decoded_message}"

if _name_ == '_main_':
    app.run(debug=True)
           
    
   
