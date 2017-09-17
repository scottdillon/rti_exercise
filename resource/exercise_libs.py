import pandas as pd
import numpy as np
import plotly as plt
import sqlalchemy as sql

SQLITE_FILE = 'exercise01.sqlite'
QUERY_FILE  = 'records_flatten.sql'
CSV_FILE    = 'exercise_records.csv'


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
            dataframe = pd.read_sql_query(self.query, conn)
        self.query_dataframe = dataframe

    def write_csv(self):
        """
        Write the csv file using pd.DataFrame.to_csv method.
        :return: None
        """
        self.query_dataframe.to_csv(self.csv_filename, index=False)


class DataProcessor(object):
    """
    Loads data from the csv file, processes it and then makes that data available
    via json.
    """
    def __init__(self, csv_file=CSV_FILE):
        pass



def write_csv_file():
    csv = CSVWriter()
    csv.fill_dataframe()
    csv.write_csv()


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


def get_database_engine(sql_file_path):
    """
    Instantiate and return a sqlalchemy database engine
    :param sql_file_path: the filepath/name of the sqlite db.
    :return: instantiated sqlalchemy engine
    """
    conn_string = 'sqlite:///{}'.format(sql_file_path)
    engine = sql.create_engine(conn_string)
    return engine


if __name__ == '__main__':
    write_csv_file()