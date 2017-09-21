import numpy as np
import plotly as plt
from .resource import exercise_libs as el

"""
These are the file names of the files needed to complete 
tasks in the exercise_libs.py module.
"""
SQLITE_FILE = 'exercise01.sqlite'
QUERY_FILE  = 'records_flatten.sql'
CSV_FILE    = 'exercise_records.csv'


sqlite_file = el.get_full_path(SQLITE_FILE)
query_file = el.get_full_path(QUERY_FILE)
csv_file = el.get_full_path(CSV_FILE)


def write_csv_file():
    """
    Open the database, query it and write the csv file.
    This writes into the resource directory instead of the
    current path.
    :return:
    """
    el.write_csv_file(sqlite_file=sqlite_file,
                      query_file=query_file,
                      csv_file=csv_file)


def load_csv_data():
    """
    Now, load the csv file into a dataframe for
    processing, etc.
    :return:
    """
    csv = el.CSVLoader(csv_file).dataframe
    data_proc = el.DataProcessor(csv)
    data_proc.create_married_column()
    return data_proc

# We don't need to execute this again. The csv file is
# already written. Let's make this depend on an argument?
# write_csv_file()


def get_index_text():
    """
    Perform some grouping on the data and return table html from
    dataframes.
    :return: a tuple of html strings which are tables.
    """
    aggregate_funcs = {'Married': ['count'],
                       'Age': ['mean'],
                       'Hours Per Week': ['mean'],
                       'Education Num': ['mean']}

    summary = data_processor.describe_census_data()
    summary_html = el.change_table_css_class(summary)
    gb_over_50k_race = data_processor.groupby_50k_married_race()
    df_over_50k = data_processor.aggregate_groupby(gb_over_50k_race, aggregate_funcs)
    html_over_50k = el.change_table_css_class(df_over_50k)
    return summary_html, html_over_50k


def hours_worked_plot():
    """
    Creates a plot of hours worked for all ages. There should be a boxplot with a box
    for each age and an average trace for the average for that age.
    
    DO NOT add a scatter object for each age value. There are 48k values and the javascript
    takes forever on slow computers (i.e. my work laptop) Chrome profiled this process as 
    taking 33s while the page took 2.5s to reload when the original hours/age scatter trace is
    removed.
    :return:
    """
    quantile_hours_worked = data_processor.get_quantile_traces()
    mean_hours_worked = data_processor.get_mean_trace()
    quantile_hours_worked.append(mean_hours_worked)
    layout = el.HoursWorkedLayout()
    fig = el.PlotlyFigure(data=quantile_hours_worked, layout=layout)
    div = el.get_plotly_div_str(figure_obj=fig)
    return div


def histogram_hours_worked():
    """
    Execute functions to manipulate data and
    create histogram plots of hours worked.
    :return:
    """
    over_50kdf, under_50k_df = data_processor.get_histo_hours_worked_data()
    histo_traces = el.get_histo_hours_worked_traces(over_50kdf, under_50k_df)
    layout = el.HistogramLayout()
    figure = el.PlotlyFigure(data=histo_traces, layout=layout)
    div = el.get_plotly_div_str(figure_obj=figure)
    return div


def over_50k_country_origin():
    origins_dataframe = data_processor.get_country_data()
    choropleth_obj = el.ChoroplethOrigins(z=origins_dataframe)
    choro_layout = el.ChoroLayout()
    figure = el.PlotlyFigure(data=[choropleth_obj],
                             layout=choro_layout)
    div = el.get_plotly_div_str(figure_obj=figure)
    return div

data_processor = load_csv_data()