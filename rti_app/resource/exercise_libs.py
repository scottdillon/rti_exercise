"""
Author: Scott Dillon
Email: scott.dillon@gmail.com

This is a collection of classes and functions to perform requirements
of the exercise as far as the data extraction, saving, csv file reading
and loading goes. Dataframe processing code is also here.

To use:
This code should be imported into core.py or views.py, etc. not executed here.

Warnings:
Importing my_app from the package will cause a circular import error.
"""
import os
import itertools as it
import numpy as np
import pandas as pd
import plotly as plt
import plotly.graph_objs as go
import sqlalchemy as sql

AGE = 'Age'
HOURS_PER_WEEK = 'Hours Per Week'
OVER_50K = 'Over 50K'


class Colors(object):
    """
    Colors taken from the default colors for the Seaborn
    package. I provide an iterator here for cycling through
    the colors using:

    colors = Colors()
    new_color = colors.next_color()

    """
    BLUE       = 'rgba(76,  114, 176, 1.0)'
    GREEN      = 'rgba(85,  168, 104, 1.0)'
    RED        = 'rgba(196,  78,  82, 1.0)'
    PURPLE     = 'rgba(129, 114, 178, 1.0)'
    YELLOW     = 'rgba(204, 185, 116, 1.0)'
    TURQUOISE  = 'rgba(100, 181, 205, 1.0)'
    BLACK      = 'rgba(  0,   0,   0, 1.0)'
    LIGHT_GRAY = 'rbga(240, 240, 240, 1.0)'

    def __init__(self):
        """
        Set up a list of colors to cycle through or select from
        and create a cycling iterator to continuously cycle colors.
        """
        self._seaborn_colors = [self.RED, self.BLUE, self.GREEN,
                                self.PURPLE, self.YELLOW, self.TURQUOISE]
        self._seaborn_cycle = it.cycle(self._seaborn_colors)

    @property
    def seaborn_colors(self):
        """
        Return the colors in a list except for light gray.
        :return:
        """
        return self._seaborn_colors

    def next_color(self):
        """
        Return the next color in the color cycle based on the
        order in the seaborn_colors attribute.
        :return:
        """
        return next(self._seaborn_cycle)


class CSVWriter(object):
    """
    Contains methods for opening database, gets teh data into
    a pandas dataframe and then saves that file as a flat
    CSV file.
    """
    def __init__(self, db_file, query_file, csv_file):
        self.engine = get_database_engine(db_file)
        self.query = get_file_contents(query_file)
        self.csv_filename = csv_file
        self.query_dataframe = None

    def fill_dataframe(self):
        """
        Make connection to database, execute the select query and fill a
        dataframe with query data.
        :return: None
        """
        with self.engine.connect() as conn:
            self.query_dataframe = pd.read_sql_query(self.query, conn)

    def write_csv(self):
        """
        Write the csv file using pd.DataFrame.to_csv method.
        :return: None
        """
        self.query_dataframe.to_csv(self.csv_filename, index=False)


class CSVLoader(object):
    """
    Loads data from the csv file into a dataframe, processes it and then makes that data available
    via json.
    """
    def __init__(self, csv_file):
        self._dataframe = None
        self.dataframe = csv_file

    @property
    def dataframe(self):
        """
        Return the dataframe .
        :return:
        """
        return self._dataframe

    @dataframe.setter
    def dataframe(self, csv_file):
        """
        Automatically convert the csv file path string into a
        dataframe since that's always what we'll need.
        :param csv_file: a file path to our csv string.
        :return:
        """
        self._dataframe = pd.read_csv(csv_file)


class DataProcessor(object):
    """
    Performs processing of the census sample dataframe and provides
    methods for returning table data.
    """
    def __init__(self, census_data_df):
        """
        Let's go ahead and assign the census data as an attribute and
        fix the column names implicitly.
        :param census_data_df: a dataframe containing the census data.
        """
        self.census_data = census_data_df
        self.list_pages = None
        self.over_50k_df = None
        self.under_50k_df = None
        self.fix_names()

    def fix_names(self):
        """
        Remove the underscores from columns names and put
        them in title case.
        :return:
        """
        new_columns = [col.replace('_', ' ').title() for col in self.census_data.columns]
        self.census_data.columns = new_columns

    def create_married_column(self):
        """
        Consolidate 'Marital Status' values into a single 'Married' column
        with a 1 or 0 indicating True or False
        :return:
        """
        all_marital_status = self.census_data.loc[:, 'Marital Status'].unique()
        married = filter(is_record_married, all_marital_status)
        self.census_data = self.census_data.assign(Married=self.census_data['Marital Status'].isin(married))

    def paginate_dataframe(self, page_length):
        """
        Split the census dataframe up into many smaller dataframes
        based on how many rows per page is desired.

        For example, if the dataframe has 25 records in it and we want 10 records per
        page, we would get a list with 3 dataframes in it.
        [10, 10 and 5]

        :param page_length: an integer for how many records we want to
         display per page.
        :return: None
        """
        df_length = len(self.census_data)
        df = self.census_data.replace('?', '')
        self.list_pages = [df.loc[i : i + page_length] for i in range(0, df_length, page_length)]

    def describe_census_data(self, decimals=3):
        """
        returns count, mean, std, min, max and quartile info on
        continuous columns in dataframe.
        :param decimals: how many decimals to round the
        results to
        :return: Returns a pd.DataFrame.
        """
        return round_decimals(self.census_data.describe(), decimals)

    def groupby_50k_married_race(self):
        """
        Perform a groupby on the dataframe with the
        columns "Over 50K" and "Race"
        :return:
        """
        groupby_cols = ['Over 50K', 'Married', 'Race']
        return self.groupby(groupby_cols)

    def groupby(self, groupby_cols):
        """
        perform a groupby on the census data with the given
        group by columns
        :param groupby_cols: a list of column names
        :return:
        """
        return self.census_data.groupby(groupby_cols)

    @staticmethod
    def aggregate_groupby(groupby_obj, agg_dict):
        """
        Perform the aggregate calculations on teh groupby
        object.
        :param groupby_obj:
        :param agg_dict: a dict with columns as keys and a list of
         string aggregation functions, i.e. 'mean', 'count'
         A valid dict would be:
         {
            'Married': ['count'],
            'Age': ['mean'],
            'Hours Per Week': ['mean'],
            'Education Num': ['mean']
         } assuming those columns are not grouping columns.
        :return:
        """
        return round_decimals(groupby_obj.agg(agg_dict), decimals=2)

    def get_quantile_traces(self):
        """
        Calculate teh quantiles for hours worked for the entire
        dataset. The create scatter objs from them and return.
        :return:  a list of scatter objs from the quantiles of
        hours worked by age.
        """
        quantiles = [0.1, 0.25, 0.50, 0.75, 0.9]
        quantiles_gb = self.perform_quantile_calculations(quantiles)
        quantile_traces = make_quantile_traces(quantiles, quantiles_gb)
        return quantile_traces

    def perform_quantile_calculations(self, quantiles):
        """
        Do age groupby then get the quantiles and re-order the
        hiearchical labels to select by quantile.
        :param quantiles: a list of decimal values
        :return: return the groupby objects
        """
        groupby = self.groupby([AGE])
        quantiles_gb = groupby[HOURS_PER_WEEK].quantile(quantiles)
        quantiles_gb = quantiles_gb.reorder_levels([1, 0])
        return quantiles_gb

    def get_mean_trace(self):
        """
        Calculate the mean hours per week and get a scatter trace
        with it
        :return:  a plotly scatter obj
        """
        agg_dict = {HOURS_PER_WEEK: np.mean}
        groupby = self.groupby([AGE])
        mean_hours_worked = self.aggregate_groupby(groupby, agg_dict)
        mean_x = mean_hours_worked.index.values
        mean_y = mean_hours_worked[HOURS_PER_WEEK].values
        mean_hours_worked_trace = AvgHoursWorkedTrace(mean_x, mean_y)
        return mean_hours_worked_trace

    def get_histo_hours_worked_data(self):
        """
        calculate the truth table of records who makes more than
        50k per year. Filter the entire dataframe for over and under
        50k and return those dataframes.
        :return:
        """
        over_50k_truth_table = self.census_data.loc[:, OVER_50K] == 1
        self.over_50k_df = self.census_data.loc[over_50k_truth_table]
        over_50k_df = self.over_50k_df[HOURS_PER_WEEK]
        under_50k_df = self.census_data[HOURS_PER_WEEK].loc[~over_50k_truth_table]
        return over_50k_df, under_50k_df

    def get_country_data(self):
        """
        Get a count of where records are form who make
        more than 50k.

        :return: returns a dataframe of counts by country
        """
        over_50k_tt = ~self.over_50k_df['Country'].isin(['United-States', '?'])
        over_50k_origins = self.over_50k_df[over_50k_tt]
        over_50k_origins_gb = over_50k_origins.groupby(['Country'])
        over_50k_origins_count = over_50k_origins_gb['Country'].count()
        return over_50k_origins_count


class GenericScatterTrace(go.Scatter):
    """
    This is a generic scatter trace inheriting from go.Scatter. Any common attributes 
    could be assigned here if they'll be set for all scatter traces.
    
    Unfortunately, we can't use property decorator since plotly won't let us add
    new attributes to graph_obj (go.*) objects. It checks this in the 
    PlotlyDict.__setitem__ method. It would be nice to set up a function 
    to check if x is a dataframe and just take the index or the values for x and y respec.
    
    I _could_ override the __setitem__ method but that _could_ also break the crap out
    of the Scatter obj/plotly so let's don't and say we didn't.
    """
    def __init__(self, x=None, y=None, marker_size=5):
        super().__init__(x=x, y=y)
        self.x = x
        self.y = y
        self.marker.size = marker_size


class HoursWorkedQuantileTrace(GenericScatterTrace):
    """
    Handles and sets standard attributes for the hours worked trace of all the hours
    worked records. This would be more useful if it were'nt a one off and we 
    were doing lots of scatter traces. Then we could set standard attributes of the
    trace for lots of plots.
    """
    opacity_dict = {'0.1' : 0.3,
                    '0.25': 0.7,
                    '0.5' : 1.0,
                    '0.75': 0.7,
                    '0.9' : 0.3}

    def __init__(self, x=None, y=None, quantile=None):
        super().__init__(x=x, y=y)
        self.mode = 'lines+markers'
        self.marker.color = Colors.BLUE
        self.marker.opacity = self.opacity_dict[str(quantile)]
        self.opacity = self.opacity_dict[str(quantile)]
        self.name = '{} Quantile'.format(quantile)


class AvgHoursWorkedTrace(GenericScatterTrace):
    """
    Contains attributes specific to the mean hours worked trace on the hours worked plot.
    Set this to use lines and markers.
    """
    def __init__(self, x=None, y=None, marker_size=8):
        super().__init__(x=x, y=y)
        self.mode = 'lines+markers'
        self.marker.color = Colors.RED
        self.marker.size = marker_size
        self.name = 'Mean hours worked<br>at each age'


class HoursWorkedLayout(go.Layout):
    """
    The plotly template object of the hours worked plot.
    
    Inherits from plotly.graph_objs.Layout object.
    """
    def __init__(self, height=600):
        super().__init__()
        self.title = "<b>Hours Per Week Worked by Age</b><br><i>with average hours worked by age</i>"
        self.yaxis.title = HOURS_PER_WEEK
        self.xaxis.title = AGE
        self.height = height


class PlotlyFigure(go.Figure):
    """
    the hours worked scatter figure with go.Data object
    conversion and sets the layout.
    """
    def __init__(self, data=None, layout=None):
        super().__init__()
        self.data = go.Data(data)
        self.layout = layout


class HistogramHoursWorked(go.Histogram):
    """
    Histogram object to use. The bin sizing requires both
    the autobinx to be false and the dict set for xins.

    We use the colors class attribute to give both
    attributes different colors without having to set them
    manually. We're also using norm to set this to a probability
    histogram intead of a count.
    """
    colors = Colors()

    def __init__(self, name=None, x=None, opacity=0.5,
                 line_width=1, norm='probability'):
        super().__init__()
        self.x = x
        self.opacity = opacity
        self.histnorm = norm
        self.autobinx = False
        self.xbins = {'start': 0, 'end': 100, 'size': 3}
        self.name = name
        self.marker.line.width = line_width
        self.marker.color = self.colors.next_color()


class HistogramLayout(go.Layout):
    """
    Subclass the layout for the histogram with default titles.
    barmode is 'overlay' so that the two histograms will be overlaid and
    not side by side.
    """
    def __init__(self, height=600):
        super().__init__()
        self.barmode = 'overlay'
        self.title = "<b>Probability Histogram of Hours Worked Per Week for<br>People with Incomes over and under 50k</b>"
        self.xaxis.title = 'Hours Worked per Week'
        self.yaxis.title = 'Probability of Working X Hours Per Week'
        self.height = height


class ChoroplethOrigins(go.Choropleth):
    """
    subclass the choropleth graph obj to assign
    attrs automatically. Important attrs here are
    locationmode, locations, z and text
    """
    def __init__(self, z=None):
        super().__init__()
        self.locations = z.index
        self.locationmode = 'country names'
        self.z = z
        self.text = z.index
        self.marker.line.color = Colors.LIGHT_GRAY


class ChoroLayout(go.Layout):
    """
    A layout for the choropleth plot with project defaults.
    """
    def __init__(self, height=500):
        super().__init__()
        self.height = height
        self.geo.showframe = True
        self.geo.showcoastlines = True
        self.geo.projection.type = 'Mercator'
        self.title = "<b>Home Country of Respondents Who Make<br>More Than $50K</b>"


def write_csv_file(sqlite_file, query_file, csv_file):
    """
    Get the data from the SQLite database into a dataframe and
    then save as a CSV.

    The default options are used for the CSVWriter object and fill_dataframe
    methods but they could be assigned here or used with
    different values elsewhere.
    :return: Nada
    """
    csv = CSVWriter(db_file=sqlite_file, query_file=query_file, csv_file=csv_file)
    csv.fill_dataframe()
    csv.write_csv()


def get_database_engine(sql_file_path):
    """
    Instantiate and return a sqlalchemy database engine
    :param sql_file_path: the filepath/name of the sqlite db.
    :return: instantiated sqlalchemy engine
    """
    conn_string = 'sqlite:///{}'.format(sql_file_path)
    engine = sql.create_engine(conn_string)
    return engine


def get_file_contents(file_path) -> str:
    """
    Opens a file and returns leading and trailing
    whitespace stripped documents.
    :param file_path: filepath string. Should simply be the name of
        sql file.
    :return: string
    """
    with open(file_path) as file:
        query = file.read()
    return query.strip()


def round_decimals(dataframe, decimals=3):
    """
    Rounds the decimals in teh dataframe to the
    given number of decimal places.
    :param dataframe: a pandas dataframe with float
    values in a column.
    :param decimals: an integer
    :return: return a dataframe with float values
    rounded to 3 decimals.
    """
    return dataframe.round(decimals)


def change_table_css_class(dataframe, index=True):
    """
    Changes out segments of html based on what is in the dict.
    :param dataframe: a dataframe to turn into html
    :return: returns table html based on the input dataframe.
    """
    css_change_dict = {'class="dataframe"': 'class="table table-sm table-striped table-hover table-bordered"',
                       'border="1"': ''}
    table_html = return_dataframe_html(dataframe, print_index=index)
    for old, new in css_change_dict.items():
        table_html = replace_css_class(table_html, old, new)
    return table_html


def return_dataframe_html(dataframe, print_index=False):
    """
    Returns the html markup from a dataframe with a
    couple of non-default options. Don't print the index
    labels and make the column names bold.

    index=False prevents the dataframe index from
    being included in the CSV.
    :param dataframe: a pandas dataframe
    :return: a str of html markup
    """
    df_html = dataframe.to_html(index=print_index)
    return df_html


def replace_css_class(html_string, old_class, new_class):
    """
    Replaces the css class in teh html element string.
    :param html_string: a string of html
    :param old_class: the text segment to replace. It should be a css class designator
    :param new_class: the text to add in place of the old css class 
    :return: a string of html
    """
    return html_string.replace(old_class, new_class)


def load_csv_file(csv_path):
    """
    Load the CSV file with the default filepath.
    :return: return a dataframe with data loaded into it.
    """
    csv = CSVLoader(csv_path)
    return csv.dataframe


def is_record_married(status):
    """
    does the status begin with the word Married
    :param status: a string representing the marital status
    :return: a boolean
    """
    return status.startswith('Married')


def get_full_path(file_name):
    """
    Get the full path for a file based on this file's directory. 
    Simply joins a filename with the directory of the file this function is in.
    :param file_name: a string object file name.
    :return: return a full absolute path string.
    """
    module_path = os.path.abspath(__file__)
    module_dir = os.path.dirname(module_path)
    return os.path.join(module_dir, file_name)


def get_plotly_div_str(figure_obj, image_height=800):
    """
    Gets the html for the div created by the plotly plot.
    :param figure_obj: a plotly graph_objs Figure object with data and layout objects
    :param image_height: an integer for the image height
    :return: returns a string of html wrapped in a div element.
    """
    return plt.offline.plot(figure_obj,
                            include_plotlyjs=False,
                            output_type='div',
                            show_link=False,
                            image_height=image_height)


def make_quantile_traces(quantile_list, quantiles_gb):
    """
    Calculate and return quantiles.
    The quantiles are in the top level of the hiearchical index.

    :param quantile_list: A list of decimal values which are the quantiles
        values  we want ot calculate.
    :param quantiles_gb: the dataframe groupby object we'll locate the
        quantiles values in.
    :return:
    """
    q_traces = []
    for q in quantile_list:
        x = quantiles_gb.loc[q].index.values
        y = quantiles_gb.loc[q].values
        trace = HoursWorkedQuantileTrace(x=x, y=y, quantile=q)
        q_traces.append(trace)
    return q_traces


def get_histo_hours_worked_traces(over_50k_df, under_50k_df):
    """
    Gets histogram objects from passed dataframes.
    :param over_50k_df: a pandas dataframe.
    :param under_50k_df: a pandas dataframe.
    :return:
    """
    over_50k_histo = HistogramHoursWorked(x=over_50k_df, name='Over $50K')
    under_50k_histo = HistogramHoursWorked(x=under_50k_df, name='Under $50K')
    return [over_50k_histo, under_50k_histo]


if __name__ == '__main__':
    pass
