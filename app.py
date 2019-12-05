import os
import controllers
from flask import Flask
from flask_bootstrap import Bootstrap


# def create_app(test_config=None):
# create and configure the app
test_config = None
app = Flask(__name__, instance_relative_config=True)
bootstrap = Bootstrap(app)
app.config.from_mapping(
    SECRET_KEY=os.getenv('SECRET_KEY'),
    DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
)

if test_config is None:
    # load the instance config, if it exists, when not testing
    app.config.from_pyfile('config.py', silent=True)
else:
    # load the test config if passed in
    app.config.from_mapping(test_config)

# ensure the instance folder exists
try:
    os.makedirs(app.instance_path)
except OSError:
    pass

# from . import controllers
app.register_blueprint(controllers.bp)
app.add_url_rule('/', endpoint='index')
app.add_url_rule('/elections', endpoint='get_elections')
app.add_url_rule('/senators', endpoint='get_senators')
app.add_url_rule('/submit_state_senators', endpoint='submit_for_state_senators')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
