import pytest
import logging
from sqlalchemy import Column, String, Integer, inspect, select
import datetime as dt

from covidvaccinationproject.util import webservice

from covidvaccinationproject.util.logger import logconfig

logconfig.setup_logging()
logging.getLogger('covidvaccinationproject.util.sqlconnector').setLevel(logging.DEBUG)


def test_country_list():
    country_list = webservice.get_country_list()

    assert country_list[0] == {'country_id': 'AFG', 'country': 'Afghanistan'}


def test_country_metric():
    country_metric_list = webservice.get_country_demographics()

    assert len(country_metric_list) > 1

    country_metric_list_filtered = webservice.get_country_demographics('AFG')

    assert len(country_metric_list_filtered) == 1
    assert country_metric_list[0]['country_id'] == 'AFG'


def test_covid_data():
    covid_data = webservice.get_covid_data('MEX')
    assert covid_data[0]['country_id'] == 'MEX'

    covid_data = webservice.get_covid_data(start_date='2020-12-30', end_date='2020-12-31')
    assert len(covid_data) > 1

    covid_data = webservice.get_covid_data('MEX', '2020-12-30', '2021-01-04', 1)
    assert covid_data[0]['date'] == dt.datetime(2021, 1, 3)


def test_covid_variant():
    covid_variant = webservice.get_variant_data('MEX')
    assert covid_variant[0]['country_id'] == 'MEX'

    covid_data = webservice.get_variant_data(start_date='2020-12-20', end_date='2020-12-31')
    assert len(covid_data) > 1

    covid_data = webservice.get_variant_data('MEX', '2020-12-20', '2021-01-05', 1)
    assert covid_data[0]['date'] == dt.datetime(2021, 1, 4)

