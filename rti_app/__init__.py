import flask

my_app = flask.Flask(__name__)
my_app.config.from_object('rti_app.config')
from rti_app import views, models


@my_app.errorhandler(404)
def not_found(error):
  return flask.render_template('404.html'), 404






