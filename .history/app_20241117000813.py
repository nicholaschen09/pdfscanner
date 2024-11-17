from flask import Flask, request, render_template
import pytesseract
from PIL import Image
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def upload_file():
    return render_template('upload.html')

@app.route('/uploader', methods=['POST'])
def uploader_file():
    if 'file' not in request.files:
        return 'No file part'
    file = request.files['file']
    if file.filename == '':
        return 'No selected file'
    if file:
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)
        text = pytesseract.image_to_string(Image.open(filepath))
        return render_template('result.html', text=text)

if __name__ == '__main__':
    app.run(debug=True)

# templates/upload.html
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <title>Upload Document</title>
  </head>
  <body>
    <h1>Upload Document</h1>
    <form action="/uploader" method="post" enctype="multipart/form-data">
      <input type="file" name="file">
      <input type="submit" value="Upload">
    </form>
  </body>
</html>

# templates/result.html
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <title>Extracted Text</title>
  </head>
  <body>
    <h1>Extracted Text</h1>
    <p>{{ text }}</p>
  </body>
</html>