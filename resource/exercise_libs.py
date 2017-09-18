import itertools as it
import pandas as pd
import numpy as np
import plotly as plt
import sqlalchemy as sql

"""
Author: Scott Dillon
Email: scott.dillon@gmail.com

This is a collection of classes and functions to perform requirements 
of the exercise as far as the data extraction, saving, csv file reading
and loading goes. Dataframe processing code is also here.
"""

SQLITE_FILE = 'exercise01.sqlite'
QUERY_FILE  = 'records_flatten.sql'
CSV_FILE    = 'exercise_records.csv'


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
        self._seaborn_colors = [self.RED, self.BLUE, self.GREEN, self.PURPLE, self.YELLOW, self.TURQUOISE]
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
    def __init__(self, db_file=SQLITE_FILE, query_file=QUERY_FILE, csv_file=CSV_FILE):
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
    def __init__(self, csv_file=CSV_FILE):
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
    def __init__(self, census_data):
        """
        Let's go ahead and assign the census data as an attribute and
        fix the column names implicitly.
        :param census_data:
        """
        self.census_data = census_data
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
        all_marital_status = self.census_data.loc['Marital Status'].unique()
        married = filter(is_record_married, all_marital_status)
        self.census_data.assign(Married=self.census_data['Marital Status'].isin(married))

    def describe_census_data(self, decimals=3):
        """
        returns count, mean, std, min, max and quartile info on
        continuous columns in dataframe.
        :param decimals: how many decimals to round the
        results to
        :return: Returns a pd.DataFrame.
        """
        return round_decimals(self.census_data.describe(), decimals)

    def groupby_50k_race(self):
        """
        Perform a groupby on the dataframe with the
        columns "Over 50K" and "Race"
        :return:
        """
        groupby_cols = ['Over 50K', 'Race']
        return self.groupby(groupby_cols)

    def groupby(self, groupby_cols):
        """
        perform a groupby on the census data with the given
        group by columns
        :param groupby_cols: a list of column names
        :return:
        """
        return self.census_data.groupby(groupby_cols)



def write_csv_file():
    """
    Get the data from the SQLite database into a dataframe and
    then save as a CSV.

    The default options are used for the CSVWriter object and fill_dataframe
    methods but they could be assigned here or used with
    different values elsewhere.
    :return: Nada
    """
    csv = CSVWriter()
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


def return_dataframe_html(dataframe):
    """
    Returns the html markup from a dataframe with a
    couple of non-default options. Don't print the index
    labels and make the column names bold.

    :param dataframe: a pandas dataframe
    :return: a str of html markup
    """
    return dataframe.to_html(bold_rows=True, index=False)


def load_csv_file():
    """
    Load the CSV file with the default filepath.
    :return:
    """
    csv = CSVLoader()
    return csv


def is_record_married(status):
    if "Married" == status[:7]:
        return True
    return False


if __name__ == '__main__':
    write_csv_file()
