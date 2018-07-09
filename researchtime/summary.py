from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, send_from_directory
)
from flask import current_app as app
from werkzeug.exceptions import abort
from werkzeug.utils import secure_filename
import os
from os.path import abspath
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer 
from sumy.summarizers.lex_rank import LexRankSummarizer
import random
import textract

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'doc', 'docx', 'html', 'htm', 'epub'])

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def summarize(text):
    parser = PlaintextParser.from_string(text, Tokenizer('english'))
    summarizer = LexRankSummarizer()
    summary = summarizer(parser.document, 5)
    summarized = []
    for sentence in summary:
        summarized.append(str(sentence))
    return summarized

bp = Blueprint('summary', __name__)
@bp.route('/', methods=['GET', 'POST'])
def index():
    processed = ''
    if request.method == 'POST':
        if 'compare' in request.form:
            raw_text = request.form['text']
            if raw_text != '':
                processed = summarize(raw_text)
                return render_template('summary/processed.html', processed = processed)
        elif 'upload' in request.form:
            if 'file' not in request.files:
                flash('No file part')
                return redirect(request.url)
            file = request.files['file']
            if file.filename == '':
                flash('No selected file')
                return redirect(request.url)
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                basedir = os.path.abspath(os.path.dirname(__file__))
                file.save(os.path.join(basedir, app.config['UPLOAD_FOLDER'], filename))

                tobeprocessed = textract.process(url_for('summary.uploaded_file', filename=filename))
                processed = summarize(tobeprocessed)

                return render_template('summary/processed.html', processed = processed)

    return render_template('summary/index.html', processed = processed)

@bp.route('/textsummary')
def textsummary():
    return render_template('summary/processed.html')

@bp.route('/tmp/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
