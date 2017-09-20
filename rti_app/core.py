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

    :return:
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

    :return:
    """
    dataframe = data_processor.census_data
    x = dataframe.loc[:, 'Age'].values
    y = dataframe.loc[:, 'Hours Per Week'].values
    mean_groupby = data_processor.groupby(['Age'])
    agg_dict = {'Hours Per Week': 'mean'}
    mean_hours_worked = data_processor.aggregate_groupby(mean_groupby, agg_dict)
    mean_x = mean_hours_worked.index.values
    mean_y = mean_hours_worked['Hours Per Week'].values
    hours_worked_trace = el.HoursWorkedTrace(x, y)
    mean_hours_worked_trace = el.AvgHoursWorkedTrace(mean_x, mean_y)
    fig = el.HoursWorkedFigure([hours_worked_trace, mean_hours_worked_trace])
    div = el.get_plotly_div_str(fig)
    return div



data_processor = load_csv_data()