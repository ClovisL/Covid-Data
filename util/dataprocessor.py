import logging
import datetime as dt

from util import dataconnector, webservice

URL = 'https://covid.ourworldindata.org/data/owid-covid-data.json'
JSON_DATA = dataconnector.get_json_from_web(URL)


def extract_country_list():
    """ Produces a country list and metadata obtained from OWID """
    # instantiate logging
    logger = logging.getLogger(__name__)

    # instantiate country list
    country_list = []
    logger.info('Extracting country metadata')

    for key, value in JSON_DATA.items():
        country_info = {
            'country_id': key,
            'continent': value.get('continent'),
            'location': value.get('location'),
            'population': value.get('population'),
            'population_density': value.get('population_density'),
            'median_age': value.get('median_age'),
            'aged_65_older': value.get('aged_65_older'),
            'aged_70_older': value.get('aged_70_older'),
            'gdp_per_capita': value.get('gdp_per_capita'),
            'cardiovasc_death_rate': value.get('cardiovasc_death_rate'),
            'diabetes_prevalence': value.get('diabetes_prevalence'),
            'handwashing_facilities': value.get('handwashing_facilities'),
            'hospital_beds_per_thousand': value.get('hospital_beds_per_thousand'),
            'life_expectancy': value.get('life_expectancy'),
            'human_development_index': value.get('human_development_index'),
            'extreme_poverty': value.get('extreme_poverty'),
            'female_smokers': value.get('female_smokers'),
            'male_smokers': value.get('male_smokers'),
        }
        country_list.append(country_info.copy())

    return country_list


def extract_covid_data():
    """ Produces a list of dictionaries with the covid data from each date recorded by OWID """
    # instantiate logging
    logger = logging.getLogger(__name__)

    covid_data_list = []
    logger.info('Extracting covid data')

    for key, value in JSON_DATA.items():

        for data_point in value['data']:
            covid_data = {
                'country_id': key,
                'date': dt.datetime.strptime(data_point.get('date'), '%Y-%m-%d'),
                'total_cases': data_point.get('total_cases'),
                'new_cases': data_point.get('new_cases'),
                'total_cases_per_million': data_point.get('total_cases_per_million'),
                'new_cases_per_million': data_point.get('new_cases_per_million'),
                'stringency_index': data_point.get('stringency_index'),
                'new_cases_smoothed': data_point.get('new_cases_smoothed'),
                'new_deaths_smoothed': data_point.get('new_deaths_smoothed'),
                'new_cases_smoothed_per_million': data_point.get('new_cases_smoothed_per_million'),
                'new_deaths_smoothed_per_million': data_point.get('new_deaths_smoothed_per_million'),
                'total_deaths': data_point.get('total_deaths'),
                'new_deaths': data_point.get('new_deaths'),
                'total_deaths_per_million': data_point.get('total_deaths_per_million'),
                'new_deaths_per_million': data_point.get('new_deaths_per_million'),
                'reproduction_rate': data_point.get('reproduction_rate'),
                'total_vaccinations': data_point.get('total_vaccinations'),
                'people_vaccinated': data_point.get('people_vaccinated'),
                'total_vaccinations_per_hundred': data_point.get('total_vaccinations_per_hundred'),
                'people_vaccinated_per_hundred': data_point.get('people_vaccinated_per_hundred'),
                'new_vaccinations_smoothed': data_point.get('new_vaccinations_smoothed'),
                'new_vaccinations_smoothed_per_million': data_point.get('new_vaccinations_smoothed_per_million'),
                'people_fully_vaccinated': data_point.get('people_fully_vaccinated'),
                'people_fully_vaccinated_per_hundred': data_point.get('people_fully_vaccinated_per_hundred'),
                'new_vaccinations': data_point.get('new_vaccinations'),
                'new_tests': data_point.get('new_tests'),
                'total_tests': data_point.get('total_tests'),
                'total_tests_per_thousand': data_point.get('total_tests_per_thousand'),
                'new_tests_per_thousand': data_point.get('new_tests_per_thousand'),
                'tests_units': data_point.get('tests_units'),
                'excess_mortality': data_point.get('excess_mortality'),
                'new_tests_smoothed': data_point.get('new_tests_smoothed'),
                'new_tests_smoothed_per_thousand': data_point.get('new_tests_smoothed_per_thousand'),
                'positive_rate': data_point.get('positive_rate'),
                'tests_per_case': data_point.get('tests_per_case'),
                'icu_patients': data_point.get('icu_patients'),
                'icu_patients_per_million': data_point.get('icu_patients_per_million'),
                'hosp_patients': data_point.get('hosp_patients'),
                'hosp_patients_per_million': data_point.get('hosp_patients_per_million'),
                'weekly_hosp_admissions': data_point.get('weekly_hosp_admissions'),
                'weekly_hosp_admissions_per_million': data_point.get('weekly_hosp_admissions_per_million'),
                'weekly_icu_admissions': data_point.get('weekly_icu_admissions'),
                'weekly_icu_admissions_per_million': data_point.get('weekly_icu_admissions_per_million'),

            }

            covid_data_list.append(covid_data.copy())

    logger.debug(covid_data_list[0])

    return covid_data_list

# Variant data removed from GitHub
# def extract_variant_data():
#     """ produces a list of data to insert into variant data pulled from OWID csv file. The location needs to be
#     changed to a country_id """

#     logger = logging.getLogger(__name__)

#     variant_url = 'https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/variants/covid-variants.csv'
#     csv_extract = dataconnector.get_csv_from_web(variant_url)

#     covid_variant_list = []
#     logger.info('Extracting variant data')

#     country_list = webservice.get_country_list()

#     for row in csv_extract:

#         # remove blank rows and replace with 0
#         for key, value in row.items():
#             if key in ['num_sequences', 'perc_sequences', 'num_sequences_total'] and value == '':
#                 row[key] = 0

#         variant_dict = {
#             'date': dt.datetime.strptime(row.get('date'), '%Y-%m-%d'),
#             'variant': row['variant'],
#             'num_sequences': row['num_sequences'],
#             'perc_sequences': row['perc_sequences'],
#             'num_sequences_total': row['num_sequences_total']
#         }

#         for country in country_list:
#             if country['country'] == row['location']:
#                 variant_dict['country_id'] = country['country_id']
#                 break

#         covid_variant_list.append(variant_dict)

#     logger.debug(covid_variant_list[0])

#     return covid_variant_list




