from flask import Flask, render_template, request, send_file
from PIL import Image
import io

app = Flask(_name_)

# Function to hide a message inside an image
def encode_image(image, message):
    encoded = image.copy()
    width, height = image.size
    pixels = encoded.load()
    
    message += "END"  # Marker to indicate end of message
    binary_message = ''.join(format(ord(char), '08b') for char in message)
    
    index = 0
    for x in range(width):
        for y in range(height):
            if index < len(binary_message):
                r, g, b = pixels[x, y]
                r = (r & ~1) | int(binary_message[index])
                pixels[x, y] = (r, g, b)
                index += 1
            else:
                break

    return encoded

# Function to extract a hidden message from an image
def decode_image(image):
    pixels = image.load()
    width, height = image.size
    
    binary_message = ""
    for x in range(width):
        for y in range(height):
            r, g, b = pixels[x, y]
            binary_message += str(r & 1)
    
    message = ''.join(chr(int(binary_message[i:i+8], 2)) for i in range(0, len(binary_message), 8))
    
    if "END" in message:
        return message.split("END")[0]
    else:
        return "No hidden message found"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/encode', methods=['POST'])
def encode():
    image = request.files['image']
    message = request.form['message']
    
    if not image or not message:
        return "Missing image or message", 400
    
    img = Image.open(image)
    encoded_img = encode_image(img, message)
    
    img_io = io.BytesIO()
    encoded_img.save(img_io, format='PNG')
    img_io.seek(0)
    
    return send_file(img_io, mimetype='image/png', as_attachment=True, download_name="encoded_image.png")

@app.route('/decode', methods=['POST'])
def decode():
    image = request.files['image']
    
    if not image:
        return "No image uploaded", 400
    
    img = Image.open(image)
    message = decode_image(img)
    
    return f"Hidden message: {message}"

if _name_ == '_main_':
    app.run(debug=True)
