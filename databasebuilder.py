import sys

sys.path.append("..")

from util import dataprocessor
from util.sqlconnector import Table, SqlConnector


from sqlalchemy import Integer, DateTime, String, Float, Column, PrimaryKeyConstraint, Index


def _create_database():
    sql_connector = SqlConnector('covid.sql')

    return sql_connector


def _create_tables(engine):
    country_schema = {
        '__tablename__': 'country',
        '__table_args__': (Index('ix_country_location_country_id', 'location', 'country_id'),
                           {'extend_existing': True},
                           ),
        'country_id': Column(String, primary_key=True),
        'continent': Column(String, nullable=True),
        'location': Column(String, nullable=True),
        'population': Column(Integer, nullable=True),
        'population_density': Column(Float),
        'median_age': Column(Float),
        'aged_65_older': Column(Float),
        'aged_70_older': Column(Float),
        'gdp_per_capita': Column(Float),
        'cardivasc_death_rate': Column(Float),
        'diabetes_prvalence': Column(Float),
        'handwashing_facilities': Column(Float),
        'hospital_beds_per_thousand': Column(Float),
        'life_expectancy':Column(Float),
        'human_development_index': Column(Float),
        'male_smokers': Column(Float),
        'female_smokers': Column(Float),
        'extreme_poverty': Column(Float),
    }

    country = Table('country', engine, country_schema)

    country.drop_table()
    country.create_table()

    covid_data_schema = {
        '__tablename__': 'covid_data',
        '__table_args__': (PrimaryKeyConstraint('country_id', 'date'),
                           {'extend_existing': True}),
        'country_id': Column(String),
        'date': Column(DateTime),
        'total_cases': Column(Integer),
        'new_cases': Column(Integer),
        'total_cases_per_million': Column(Float),
        'new_cases_per_million': Column(Float),
        'stringency_index': Column(Float),
        'new_cases_smoothed': Column(Float),
        'new_deaths_smoothed': Column(Float),
        'new_cases_smoothed_per_million': Column(Float),
        'new_deaths_smoothed_per_million': Column(Float),
        'total_deaths': Column(Float),
        'new_deaths': Column(Float),
        'total_deaths_per_million': Column(Float),
        'new_deaths_per_million': Column(Float),
        'reproduction_rate': Column(Float),
        'total_vaccinations': Column(Float),
        'people_vaccinated': Column(Float),
        'total_vaccinations_per_hundred': Column(Float),
        'people_vaccinated_per_hundred': Column(Float),
        'new_vaccinations_smoothed': Column(Float),
        'new_vaccinations_smoothed_per_million': Column(Float),
        'people_fully_vaccinated': Column(Float),
        'people_fully_vaccinated_per_hundred': Column(Float),
        'new_vaccinations': Column(Float),
        'new_tests': Column(Float),
        'total_tests': Column(Float),
        'total_tests_per_thousand': Column(Float),
        'new_tests_per_thousand': Column(Float),
        'tests_units': Column(String),
        'excess_mortality': Column(Float),
        'new_tests_smoothed': Column(Float),
        'new_tests_smoothed_per_thousand': Column(Float),
        'positive_rate': Column(Float),
        'tests_per_case': Column(Float),
        'icu_patients': Column(Float),
        'icu_patients_per_million': Column(Float),
        'hosp_patients': Column(Float),
        'hosp_patients_per_million': Column(Float),
        'weekly_hosp_admissions': Column(Float),
        'weekly_hosp_admissions_per_million': Column(Float),
        'weekly_icu_admissions': Column(Float),
        'weekly_icu_admissions_per_million': Column(Float)

    }

    covid_data = Table('covid_data', engine, covid_data_schema)

    covid_data.drop_table()
    covid_data.create_table()

    variant_data_schema = {
        '__tablename__': 'covid_variant',
        '__table_args__': (PrimaryKeyConstraint('country_id', 'date', 'variant'),
                           {'extend_existing': True}),
        'country_id': Column(String),
        'date': Column(DateTime),
        'variant': Column(String),
        'num_sequences': Column(Integer),
        'perc_sequences': Column(Float),
        'num_sequences_total': Column(Integer)
    }

    variant_data = Table('covid_variant', engine, variant_data_schema)

    variant_data.drop_table()
    variant_data.create_table()


def _load_database(engine):

    country = Table('country', engine)

    country_data = dataprocessor.extract_country_list()
    country.insert_data(country_data)

    covid = Table('covid_data', engine)
    covid_data = dataprocessor.extract_covid_data()
    covid.insert_data(covid_data)

    variant = Table('covid_variant', engine)
    variant_data = dataprocessor.extract_variant_data()
    variant.insert_data(variant_data)


def build_database():
    conn = _create_database()
    _create_tables(conn.engine)
    _load_database(conn.engine)
