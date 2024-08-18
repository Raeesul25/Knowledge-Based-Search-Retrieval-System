import os
from flask import Flask, render_template, request, flash, url_for, redirect, jsonify
from werkzeug.utils import secure_filename
from PyPDF2 import PdfReader
from document_processor import extract_text, split_document, embed_and_store
from database import insert_document

app = Flask(__name__, template_folder='../templates', static_folder='../static')

UPLOAD_FOLDER = "D:\\Assessments\\XYGen.ai\\uploads"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ['pdf']

def get_pdf_page_count(pdf_path):
    with open(pdf_path, 'rb') as file:
        reader = PdfReader(file)
        return len(reader.pages)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        if 'file' not in request.files:
            return jsonify({"error": "No file part"}), 400
        
        file = request.files['file']
        report_type = request.form['report_type']
        notes = request.form['notes']

        if file.filename == '':
            return jsonify({"error": "No selected file"}), 400

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            print(filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            print(file_path)
            page_count = get_pdf_page_count(file_path)

            # document processor
            text = extract_text(file_path)
            print(f'extracted text length is {len(text)}')
            chunks = split_document(text)
            print(f'chunk length is {len(chunks)}')
            vector_store = embed_and_store(chunks)
            print('Sucessfully completed the document processing')
            
            # database processing
            insert_document(filename, report_type, notes, page_count, file_path)
            # flash('File successfully uploaded')
            return redirect(url_for('upload'))

    return render_template('upload.html')

@app.route('/search', methods=['GET', 'POST'])
def search():
    return render_template('search.html')

if __name__ == '__main__':
    app.run(debug=True)