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
import requests
import re
import uuid
import textract

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'doc', 'docx', 'html', 'htm', 'epub'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def summarize(text, num):
    parser = PlaintextParser.from_string(text, Tokenizer('english'))
    summarizer = LexRankSummarizer()
    summary = summarizer(parser.document, num)
    summarized = []
    for sentence in summary:
        summarized.append(str(sentence))
    return summarized

def get_filename(cd):
    if not cd:
        return None
    fname = re.findall('filename=(.+)', cd)
    if len(fname) == 0:
        return None
    return fname[0]

bp = Blueprint('summary', __name__)
@bp.route('/', methods=['GET', 'POST'])
def index():
    processed = ''
    if request.method == 'POST':
        sentenceNum = 5
        try:
            snum = int(request.form['sentNum'])
            if snum >0 and snum < 100:
                sentenceNum = snum
        except:
            sentenceNum = 5

        
        if 'compare' in request.form:
            raw_text = request.form['text']
            if raw_text != '':
                processed = summarize(raw_text, sentenceNum)
                return render_template('summary/processed.html', processed = processed)
            return ''
        elif 'upload' in request.form:
            if 'file' not in request.files:
                return 'No file'
            file = request.files['file']
            if file.filename == '':
                return 'No selected file'
            if file and allowed_file(file.filename):
                ext = file.filename.rsplit('.', 1)[1].lower()
                file.filename = str(uuid.uuid4()) + '.' + ext
                filename = secure_filename(file.filename)
                print(filename)
                basedir = os.path.abspath(os.path.dirname(__file__))
                file.save(os.path.join(basedir, app.config['UPLOAD_FOLDER'], filename))
                tobeprocessed = textract.process(url_for('summary.uploaded_file', filename=filename))
                processed = summarize(tobeprocessed, sentenceNum)

                os.remove(os.path.join(basedir, app.config['UPLOAD_FOLDER'], filename))

                return render_template('summary/processed.html', processed = processed)
            return 'File not allowed'
        elif 'external' in request.form:
            #add code to check if proper url
            link = request.form['url']
            r = requests.get(link, allow_redirects=True)
            print(r)
            print(r.headers.get('content-disposition'))
            filename = get_filename(r.headers.get('content-disposition'))
            print(filename)
            basedir = os.path.abspath(os.path.dirname(__file__))
            with open(os.path.join(basedir, app.config['UPLOAD_FOLDER'], filename), 'wb') as f:
                f.write(r.content)

            unprocessed = textract.process(url_for('summary.uploaded_file', filename=filename))
            processed = summarize(unprocessed, sentenceNum)

            os.remove(os.path.join(basedir, app.config['UPLOAD_FOLDER'], filename))

            return render_template('summary/processed.html', processed = processed)



    return render_template('summary/index.html', processed = processed)

@bp.route('/textsummary')
def textsummary():
    return render_template('summary/processed.html')

@bp.route('/tmp/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
