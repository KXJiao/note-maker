from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from flask import current_app as app
from werkzeug.exceptions import abort
from werkzeug.utils import secure_filename
import os
from os.path import abspath
#Import library essentials
from sumy.parsers.plaintext import PlaintextParser #We're choosing a plaintext parser here, other parsers available for HTML etc.
from sumy.nlp.tokenizers import Tokenizer 
from sumy.summarizers.lex_rank import LexRankSummarizer #We're choosing Lexrank, other algorithms are also built in
import textract

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'doc', 'docx', 'html', 'htm', 'epub'])

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def summarize(text):
    summarizer = LexRankSummarizer()
    summary = summarizer(text, 5)
    return summary

bp = Blueprint('summary', __name__)
@bp.route('/', methods=['GET', 'POST'])
def index():
    # if request.method == 'POST':
    #     if 'file' not in request.files:
    #         flash('No file part')
    #         return redirect(request.url)
    #     file = request.files['file']
    #     if file.filename == '':
    #         flash('No selected file')
    #         return redirect(request.url)
    #     if file and allowed_file(file.filename):
    #         filename = secure_filename(file.filename)
    #         print(file.filename)
    #         print(filename)
    #         print(app.config['UPLOAD_FOLDER'])
    #         print(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    #         basedir = os.path.abspath(os.path.dirname(__file__))
    #         file.save(os.path.join(basedir, app.config['UPLOAD_FOLDER'], filename))
    #         print(url_for('uploaded_file', filename=filename))
    #         return redirect(url_for('uploaded_file',
    #                                 filename=filename))
    return render_template('summary/index.html')

@bp.route('/process/', methods=['POST'])
def processed():
    raw_text = request.form['text']
    processed = summarize(raw_text)

    
    return render_template('summary/index.html', message = processed)
