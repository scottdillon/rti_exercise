import os
from rti_app import my_app
from flask import render_template, request
from .core import data_processor
from .resource import exercise_libs as el


@my_app.route('/')
@my_app.route('/index')
def index():
    """
    stuff
    :return:
    """
    summary = data_processor.describe_census_data()
    summary_html = el.change_table_css_class(summary)
    gb_over_50k_race = data_processor.groupby_50k_married_race()
    df_over_50k = data_processor.aggregate_groupby(gb_over_50k_race)
    html_over_50k = el.change_table_css_class(df_over_50k)
    return render_template('index.html',
                           summary_stats=summary_html,
                           over_50k_race_marr=html_over_50k)


@my_app.route('/show_data')
def show_data():
    """

    :return:
    """
    return render_template()