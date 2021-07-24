from flask import Flask, render_template, redirect, jsonify, request
import sys

sys.path.append("..")

from util.databasebuilder import build_database
from util.webservice import get_country_list, get_country_demographics, get_covid_data, get_variant_data
from util.sqlconnector import SqlConnector

from util.logger import logconfig

app = Flask(__name__)



@app.route('/')
def index():
    return render_template('index.html')


@app.route('/data/countrylist', methods=['GET'])
def country_list():
    return jsonify(get_country_list())


@app.route('/data/countrydemo', methods=['GET'])
def country_filter():
    query_parameters = request.args
    param_dict = {}

    country_id = query_parameters.get('id')

    if country_id:
        param_dict['country_id'] = country_id

    results = get_country_demographics(**param_dict)

    return jsonify(results)


@app.route('/data/coviddata', methods=['GET'])
def covid_filter():
    query_parameters = request.args
    param_dict = {}

    country_id = query_parameters.get('id')
    start_date = query_parameters.get('start_date')
    end_date = query_parameters.get('end_date')
    most_recent = query_parameters.get('most_recent')

    if country_id:
        param_dict['country_id'] = country_id
    if start_date:
        param_dict['start_date'] = start_date
    if end_date:
        param_dict['end_date'] = end_date
    if most_recent:
        param_dict['most_recent'] = most_recent

    results = get_covid_data(**param_dict)

    return jsonify(results)

@app.route('/data/variantdata', methods=['GET'])
def variant_filter():
    query_parameters = request.args
    param_dict = {}

    country_id = query_parameters.get('id')
    start_date = query_parameters.get('start_date')
    end_date = query_parameters.get('end_date')
    most_recent = query_parameters.get('most_recent')

    if country_id:
        param_dict['country_id'] = country_id
    if start_date:
        param_dict['start_date'] = start_date
    if end_date:
        param_dict['end_date'] = end_date
    if most_recent:
        param_dict['most_recent'] = most_recent

    results = get_variant_data(**param_dict)

    return jsonify(results)


if __name__ == "__main__":
    logconfig.setup_logging()
    build_database()
    app.run(debug=True)

