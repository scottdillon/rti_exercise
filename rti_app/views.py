import os
from rti_app import my_app
from flask import render_template, request
from .core import get_index_text
# from .resource import exercise_libs as el


@my_app.route('/')
@my_app.route('/index')
def index():
    """
    stuff
    :return:
    """
    summary_html, html_over_50k = get_index_text()
    return render_template('index.html',
                           summary_stats=summary_html,
                           over_50k_race_marr=html_over_50k)


@my_app.route('/show_data')
def show_data():
    """

    :return:
    """
    return render_template()