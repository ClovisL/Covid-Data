import csv
import requests
import json
import logging


class InvalidSiteError(Exception):
    """Exception raised if status code returned is 404"""
    pass


def get_json_from_web(url):
    # instantiate logger
    logger = logging.getLogger(__name__)

    r = requests.get(url)

    if not r.status_code == 200:
        raise InvalidSiteError

    return r.json()


def get_csv_from_web(url):
    """ makes a request to a csv url and returns a list of dictionaries """
    # instantiate logger
    logger = logging.getLogger(__name__)

    r = requests.get(url)

    if not r.status_code == 200:
        raise  InvalidSiteError

    decoded_content = r.content.decode('utf-8')

    csv_dict = []

    reader = csv.DictReader(decoded_content.splitlines(), delimiter = ',')
    for row in list(reader):
        csv_dict.append(row)

    logger.debug(csv_dict)

    return csv_dict
