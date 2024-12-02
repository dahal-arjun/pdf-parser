from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
import os

from dotenv import load_dotenv


from processor.file_processor import FileProcessor
from utils.parser.pdf_parser import PDFParser
from utils.writer.csv_writer import CSVWriter
load_dotenv()

# ====== Configuration ======
UPLOAD_FOLDER = os.getenv("UPLOAD_FOLDER")
ALLOWED_EXTENSIONS = os.getenv("ALLOWED_EXTENSIONS").split(',')
NO_FILE_ERROR = "No file part"
INVALID_FILE_TYPE_ERROR = "Invalid file type"


# ====== Setup ======
app = Flask(__name__)
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
file_processor = FileProcessor(PDFParser(), CSVWriter())


#====== Rules ======
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

#====== Routes ======
@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/process-pdf', methods=['POST'])
def process_pdf():
    if 'file' not in request.files:
        return NO_FILE_ERROR, 400

    pdf = request.files['file']

    if not allowed_file(pdf.filename):
        return INVALID_FILE_TYPE_ERROR, 400

    filename = secure_filename(pdf.filename)
    save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    pdf.save(save_path)

    task_id = file_processor.process_file(save_path)
    return jsonify({"task_id": task_id})


@app.route('/status/<task_id>', methods=['GET'])
def get_status(task_id):
    status = file_processor.get_status(task_id)
    return jsonify({"task_id": task_id, "status": status})


@app.route('/kill', methods=['GET'])
def close():
    file_processor.close()
    return jsonify({"message": "Processor closed"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
