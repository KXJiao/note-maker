import os

from flask import Flask
from . import summary

<<<<<<< HEAD
UPLOAD_FOLDER = '/uploads'

=======
>>>>>>> b31b7c531f473bb9bb90d4006387c3435479bfda
def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'researchtime.sqlite'),
    )
<<<<<<< HEAD
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


=======
>>>>>>> b31b7c531f473bb9bb90d4006387c3435479bfda
    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

<<<<<<< HEAD
=======
    @app.route('/hello')
    def hello():
        return 'hello world'
>>>>>>> b31b7c531f473bb9bb90d4006387c3435479bfda

    app.register_blueprint(summary.bp)
    app.add_url_rule('/', endpoint='index')

    return app
