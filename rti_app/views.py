from rti_app import my_app
from flask import render_template, request
from .core import get_index_text, hours_worked_plot
from .core import histogram_hours_worked, over_50k_country_origin
from .core import data_processor


@my_app.route('/')
@my_app.route('/index')
def index():
    """
    stuff
    :return:
    """
    summary_html, html_over_50k = get_index_text()
    hours_worked_div = hours_worked_plot()
    histogram = histogram_hours_worked()
    choropleth = over_50k_country_origin()
    return render_template('index.html',
                           summary_stats=summary_html,
                           over_50k_race_marr=html_over_50k,
                           hours_worked=hours_worked_div,
                           histogram_hours_worked=histogram,
                           map_over50k=choropleth)


@my_app.route('/show_data')
def show_data():
    """

    :return:
    """
    cen_dataframe = data_processor.census_data
    PAGE_LENGTH = 20



    return render_template('show_data.html',
                           census_table=page_html)
