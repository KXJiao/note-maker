from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from flask import current_app as app
from werkzeug.exceptions import abort
from werkzeug.utils import secure_filename
import os
import textract

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'doc', 'docx', 'html', 'htm', 'epub'])

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

bp = Blueprint('summary', __name__)
@bp.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            print(file.filename)
            print(filename)
            print(app.config['UPLOAD_FOLDER'])
            print(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            #file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            file.save(app.config['UPLOAD_FOLDER'])
            print(url_for('uploaded_file', filename=filename))
            return redirect(url_for('uploaded_file',
                                    filename=filename))
    
    return render_template('summary/index.html')
