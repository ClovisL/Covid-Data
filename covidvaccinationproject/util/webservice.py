from sqlalchemy import select, func, and_
from sqlalchemy.orm import sessionmaker
import logging
import datetime as dt

from covidvaccinationproject.util.sqlconnector import Table, SqlConnector


def get_country_list():
    logger = logging.getLogger(__name__)

    conn = SqlConnector('covid.db')
    country_list= []

    country_table = Table('country', conn.engine)

    Session = sessionmaker(bind=conn.engine)
    session = Session()

    query = session.query(country_table.table.c.country_id, country_table.table.c.location)

    for country in query:
        country_list.append({
            'country_id': country[0],
            'country': country[1]
        })

    logger.debug(country_list)

    session.close()

    return country_list


def get_country_demographics(country_id=None):
    logger = logging.getLogger(__name__)

    conn = SqlConnector('covid.db')
    country_demo_list = []

    country_table = Table('country', conn.engine)

    Sesssion = sessionmaker(bind=conn.engine)
    session = Sesssion()

    if country_id:
        query = session.query(country_table.table).filter(country_table.table.c.country_id == country_id)
    else:
        query = session.query(country_table.table)

    for country in query:
        country_demo_list.append({
            'country_id': country[0],
            'continent': country[1],
            'location': country[2],
            'population': country[3],
            'median_age': country[4],
            'aged_65_older': country[5],
            'aged_70_older': country[6],
            'gdp_per_capita': country[7],
            'cardivasc_death_rate': country[8],
            'diabetes_prvalence': country[9],
            'handwashing_facilities': country[10],
            'hospital_beads_per_thousand': country[11],
            'life_expectancy': country[12],
            'human_development_index': country[13],
            'male_smokers': country[14],
            'female_smokers': country[15],
            'extreme_poverty': country[16]
        })

    logger.debug(country_demo_list)

    session.close()

    return country_demo_list


def get_covid_data(country_id=None, start_date=None, end_date=None, most_recent=None):
    logger = logging.getLogger(__name__)

    conn = SqlConnector('covid.db')
    covid_data_list = []

    covid_table = Table('covid_data', conn.engine)

    Sesssion = sessionmaker(bind=conn.engine)
    session = Sesssion()

    query = session.query(covid_table.table)

    if country_id:
        query = query.filter(covid_table.table.c.country_id == country_id)
    if start_date:
        query = query.filter(covid_table.table.c.date >= start_date)
    if end_date:
        query = query.filter(covid_table.table.c.date <= end_date)

    if most_recent:
        sub_query = query.add_columns(func.max(covid_table.table.c.date).label('most_recent_date')).\
            group_by(covid_table.table.c.country_id).subquery()

        query = query.join(sub_query, and_(covid_table.table.c.date == sub_query.c.most_recent_date, covid_table.table.c.country_id == sub_query.c.country_id))

    for data_point in query:
        covid_data_list.append({
            'country_id': data_point[0],
            'date': data_point[1],
            'total_cases': data_point[2],
            'new_cases': data_point[3],
            'total_cases_per_million': data_point[4],
            'new_cases_per_million': data_point[5],
            'stringency_index': data_point[6],
            'new_cases_smoothed': data_point[7],
            'new_deaths_smoothed': data_point[8],
            'new_cases_smoothed_per_million': data_point[9],
            'new_deaths_smoothed_per_million': data_point[10],
            'total_deaths': data_point[11],
            'new_deaths': data_point[12],
            'total_deaths_per_million': data_point[13],
            'new_deaths_per_million': data_point[14],
            'reproduction_rate': data_point[15],
            'total_vaccinations': data_point[16],
            'people_vaccinated': data_point[17],
            'total_vaccinations_per_hundred': data_point[18],
            'people_vaccinated_per_hundred': data_point[19],
            'new_vaccinations_smoothed': data_point[20],
            'new_vaccinations_smoothed_per_million': data_point[21],
            'people_fully_vaccinated': data_point[22],
            'people_fully_vaccinated_per_hundred': data_point[23],
            'new_vaccinations': data_point[24],
            'new_tests': data_point[25],
            'total_tests': data_point[26],
            'total_tests_per_thousand': data_point[27],
            'new_tests_per_thousand': data_point[28],
            'tests_units': data_point[29],
            'excess_mortality': data_point[30],
            'new_tests_smoothed': data_point[31],
            'new_tests_smoothed_per_thousand': data_point[32],
            'positive_rate': data_point[33],
            'tests_per_case': data_point[34],
            'icu_patients': data_point[35],
            'icu_patients_per_million': data_point[36],
            'hosp_patients': data_point[37],
            'hosp_patients_per_million': data_point[38],
            'weekly_hosp_admissions': data_point[39],
            'weekly_hosp_admissions_per_million': data_point[40],
            'weekly_icu_admissions': data_point[41],
            'weekly_icu_admissions_per_million': data_point[42]
        })

    logger.debug(covid_data_list)

    session.close()

    return covid_data_list


def get_variant_data(country_id=None, start_date=None, end_date=None, most_recent=None):
    logger = logging.getLogger(__name__)

    conn = SqlConnector('covid.db')
    variant_data_list = []

    variant_table = Table('covid_variant', conn.engine)

    Sesssion = sessionmaker(bind=conn.engine)
    session = Sesssion()

    query = session.query(variant_table.table)

    if country_id:
        query = query.filter(variant_table.table.c.country_id == country_id)
    if start_date:
        query = query.filter(variant_table.table.c.date >= start_date)
    if end_date:
        query = query.filter(variant_table.table.c.date <= end_date)

    if most_recent:
        sub_query = query.add_columns(func.max(variant_table.table.c.date).label('most_recent_date')). \
            group_by(variant_table.table.c.country_id).subquery()

        query = query.join(sub_query, and_(variant_table.table.c.date == sub_query.c.most_recent_date,
                                           variant_table.table.c.country_id == sub_query.c.country_id))

    for data_point in query:
        variant_data_list.append({
            'country_id': data_point[0],
            'date': data_point[1],
            'variant': data_point[2],
            'num_sequences': data_point[3],
            'perc_sequences': data_point[4],
            'num_sequences_total': data_point[5]
        })

    logger.debug(variant_data_list)

    session.close()

    return variant_data_list
