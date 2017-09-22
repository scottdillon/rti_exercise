from rti_app import my_app
from flask import render_template, request
from .core import get_index_text, hours_worked_plot
from .core import histogram_hours_worked, over_50k_country_origin
from .core import data_processor, chop_dataframe
from .resource.exercise_libs import change_table_css_class


@my_app.route('/')
@my_app.route('/index')
def index():
    """
    Pulls all the data and plots together for creating the index page.

    :return: renders the template and returns the html
    """
    summary_html, html_over_50k = get_index_text()
    hours_worked_div = hours_worked_plot()
    histogram = histogram_hours_worked()
    choropleth = over_50k_country_origin()
    return render_template('index.html',
                           title="RTI Exercise, Scott Dillon",
                           summary_stats=summary_html,
                           over_50k_race_marr=html_over_50k,
                           hours_worked=hours_worked_div,
                           histogram_hours_worked=histogram,
                           map_over50k=choropleth)


@my_app.route('/show_data', methods=['GET'])
@my_app.route('/show_data?page=<int:page>', methods=['GET', 'POST'])
def show_data(page=1):
    """
    Displays the paginated view of the data. There are a few things going
    on here so lets go through them.

    First, set the records to show for each page.
    Then, chop the large dataframe up if it isn't already.
    Get the page number from the query string.
    Make sure the page number is within the bounds of our page number
        which are also the indices of the data_processor.list_pages
        which is our list of smaller size databases.
    :return: render the template with our templated stuff in it.
    """
    page_length = 25

    chop_dataframe(data_processor, page_length)

    if request.args.get('page'):
        page = int(request.args.get('page'))

    first_page = 1
    last_page = len(data_processor.list_pages)
    page = sorted([first_page, page, last_page])[1]

    table_html = data_processor.list_pages[page - 1]
    table_html = change_table_css_class(table_html, index=True)
    return render_template('show_data.html',
                           title="RTI Exercise, Scott Dillon",
                           table_html=table_html,
                           page=page,
                           first_page=first_page,
                           last_page=last_page)
