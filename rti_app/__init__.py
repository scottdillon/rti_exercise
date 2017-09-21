from flask import Flask, render_template
# from flask_restful import Api

my_app = Flask(__name__)
my_app.config.from_object('rti_app.config')
# api = Api(my_app)
from rti_app import views, models


@my_app.errorhandler(404)
def not_found(error):
  return render_template('404.html'), 404






