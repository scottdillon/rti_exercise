from flask import jsonify
from rti_app import api
from flask_restful import Resource
from rti_app.core import data_processor

class CensusData(Resource):
    """ Have abandoned this because jsGrid didn't work. Doesn't fill in the values but does recognize the length
    of data and paginate correctly. Annoying."""
    def get(self):
        """
        Building a REST API: https://www.codementor.io/sagaragarwal94/building-a-basic-restful-api-in-python-58k02xsiq
        :return: 
        """
        census_df = data_processor.census_data
        # json_data = jsonify(census_df.values)
        json_data = census_df[:10].to_json(orient='records')
        return   json_data

api.add_resource(CensusData, '/show_data')