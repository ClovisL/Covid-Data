import pytest
import logging
import datetime as dt

from util import dataprocessor as dp

from util.logger import logconfig
logconfig.setup_logging()
logging.getLogger('covidvaccinationproject.util.dataprocessor').setLevel(logging.DEBUG)


def test_country_list():
    country_list = dp.extract_country_list()

    assert country_list[0]['country_id'] == 'AFG'
    assert country_list[2]['location'] == 'Albania'
    assert len(country_list) == 231


def test_covid_data():
    covid_data = dp.extract_covid_data()

    assert covid_data[0]['date'] == dt.datetime(2020, 2, 24)
    assert len(covid_data) > 100000


def test_variant_data():
    variant_data = dp.extract_variant_data()

    assert variant_data[0]['country_id'] == 'AGO'
    assert variant_data[0]['variant'] == 'B.1.160'