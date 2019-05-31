import os
from flask import Flask
from . import db

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__,instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev', DATABASE=os.path.join(app.instance_path, 'flask.sqlite')
    )
    if test_config is None:
        app.config.from_pyfile('config.py' , silent=True)
    else:
        app.config.from_mapping(test_config)
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route('/hello')
    def hello():
        return "hello"

    db.init_app(app)

    from . import auth
    app.register_blueprint(auth.bp)

    from . import blog
    app.register_blueprint(blog.bp)
    app.add_url_rule('/', endpoint='index')

    from . import demo
    app.register_blueprint(demo.dp)

    return app