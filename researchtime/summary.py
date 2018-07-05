from flask import (
	Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

bp = Blueprint('summary', __name__)
@bp.route('/')
def index():
	# blah
	return render_template('summary/index.html')
