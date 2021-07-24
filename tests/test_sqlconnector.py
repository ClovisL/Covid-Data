import pytest
import logging
from sqlalchemy import Column, String, Integer, inspect, select

from util.sqlconnector import SqlConnector, Table

from util.logger import logconfig

logconfig.setup_logging()
logging.getLogger('covidvaccinationproject.util.sqlconnector').setLevel(logging.DEBUG)


@pytest.fixture
def connector():
    return SqlConnector('test.db')


@pytest.fixture
def test_table_schema():
    return {'__tablename__': 'test_table',
            '__table_args__': {'extend_existing': True},
            'test_col_1': Column(Integer, primary_key=True),
            'test_col_2': Column(String)}


class TestSqlConnectorClass:

    def test_connect_db(self):
        connector = SqlConnector('test.db')

        try:
            conn = connector._connect_engine()
            conn.connect()
            connection_success = True
        except Exception as ex:
            connection_success = False
            print(ex)

        assert connection_success


class TestTableClass:
    def test_create_table(self, connector, test_table_schema):

        test_table = Table('test_table', connector.engine, test_table_schema)

        test_table.create_table()

        assert connector.engine.has_table('test_table')

    def test_drop_table(self, connector, test_table_schema):
        test_table = Table('test_table', connector.engine, test_table_schema)

        # create and verify table is created
        test_table.create_table()
        assert connector.engine.has_table('test_table')

        # test drop function
        test_table.drop_table()
        assert not connector.engine.has_table('test_table')

    def test_insert_data(self, connector, test_table_schema):
        test_table = Table('test_table', connector.engine, test_table_schema)

        # drop table and create table to purge data
        test_table.drop_table()
        test_table.create_table()

        # insert single row into test_table
        test_table.insert_data([{
            'test_col_1': 1,
            'test_col_2': 'one'
        }])

        # setup connection to retrieve data
        conn = connector.engine.connect()
        query = test_table.table.select()
        results = conn.execute(query).fetchall()

        # test single inserted row
        assert results == [(1, 'one')]

        # insert multiple records into table
        test_table.insert_data([{
            'test_col_1': 2,
            'test_col_2':  'two'
        }, {
            'test_col_1': 3,
            'test_col_2': 'three'
        }])

        results = conn.execute(query).fetchall()

        # test multiple rows appended to table
        assert results == [(1, 'one'),
                           (2, 'two'),
                           (3, 'three')]

    def test_drop_create(self, connector, test_table_schema):
        test_table = Table('test_table', connector.engine, test_table_schema)

        test_table.drop_table()
        test_table.create_table()

        assert connector.engine.has_table('test_table')

        test_table.drop_table()
        test_table.create_table()

        assert connector.engine.has_table('test_table')


