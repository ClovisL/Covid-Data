import logging

import pytest

from covidvaccinationproject.util import dataconnector as dc
from covidvaccinationproject.util.logger import logconfig

logconfig.setup_logging()
logging.getLogger('covidvacinationproject.util.dataconnector').setLevel(logging.DEBUG)


def test_connect_web_json():
    url = 'https://covid.ourworldindata.org/data/owid-covid-data.json'
    data = dc.get_json_from_web(url)

    assert data is not None


def test_invalid_site_error():
    url = 'http://httpbin.org/status/404'
    with pytest.raises(dc.InvalidSiteError):
        data = dc.get_json_from_web(url)


def test_connect_web_csv():
    url = 'https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/variants/covid-variants.csv'
    data = dc.get_csv_from_web(url)

    assert data is not None
    assert data[0]['location'] == 'Angola'