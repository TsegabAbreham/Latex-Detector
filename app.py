from flask import Flask, request, render_template, redirect, url_for
from werkzeug.utils import secure_filename
import os
from simple_latex_ocr.models import Latex_OCR

# Configuration
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# Ensure the upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Initialize Flask app, specifying static and template folders
app = Flask(
    __name__,
    static_folder='static',
    template_folder='templates'
)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Initialize the OCR model (loads once)
model = Latex_OCR()

# Helper to check allowed file extensions
def allowed_file(filename):
    return (
        '.' in filename and
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
    )

@app.route('/', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            # Run OCR on the saved image
            result = model.predict(filepath)
            return render_template(
                'result.html',
                formula=result.get('formula', ''),
                confidence=result.get('confidence', 0.0),
                elapse=result.get('elapse', 0.0)
            )
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)