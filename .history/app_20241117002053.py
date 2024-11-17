from flask import Flask, request, render_template, redirect, url_for
import fitz  # PyMuPDF

app = Flask(__name__)

@app.route('/')
def upload_form():
    return render_template('upload.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)
    if file:
        file_path = f'uploads/{file.filename}'
        file.save(file_path)
        text = extract_text_from_pdf(file_path)
        return render_template('result.html', text=text)

def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

if __name__ == '__main__':
    app.run(debug=True)