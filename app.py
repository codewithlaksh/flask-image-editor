from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename
import os
import cv2

app = Flask(__name__)
app.config['UPLOADS_DIR'] = os.path.join('uploads')
ALLOWED_EXT = {'jpeg', 'jpg', 'png'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXT

def processImage(filename, operation):
    image = cv2.imread(f'uploads/{filename}')
    match operation:
        case "gray":
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            newFilename = f"uploads/converts/{filename}"
            cv2.imwrite(newFilename, gray)
            return newFilename
        case "cjpg":
            newFilename = f"uploads/converts/{filename.split('.')[0] + '.jpg'}"
            cv2.imwrite(newFilename, image)
            return newFilename
        case "cwebp":
            newFilename = f"uploads/converts/{filename.split('.')[0] + '.webp'}"
            cv2.imwrite(newFilename, image)
            return newFilename
        case "cpng":
            newFilename = f"uploads/converts/{filename.split('.')[0] + '.png'}"
            cv2.imwrite(newFilename, image)
            return newFilename

@app.route("/uploads/<path:filename>")
def uploads_serve(filename):
    return send_from_directory(os.path.join(app.config['UPLOADS_DIR']), filename)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/edit", methods=["POST"])
def edit():
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    operation = request.form.get('operation')

    if file.filename == '':
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOADS_DIR'], filename))
        newFilename = processImage(filename, operation)
        return f'You file is available here: <a href="{newFilename}">here</a>'
    

if __name__ == "__main__":
    app.run(debug=True)
