from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
import logging
from pathlib import Path


class SqlConnector:

    def __init__(self, db_name):
        self._logger = logging.getLogger(__name__)
        self._db_name = db_name

        self._engine = self._connect_engine()

    @property
    def engine(self):
        return self._engine

    def _connect_engine(self):
        # get flask root level folder
        engine = None
        root_path = Path(__file__).parent.parent
        db_path = root_path / f'data/{self._db_name}'

        self._logger.info('Connecting to database')
        try:
            engine = create_engine(f'sqlite:///{db_path}')
        except Exception as ex:
            self._logger.error(ex)
            
        return engine


class Table:

    def __init__(self, table_name, engine, table_schema = None):
        self._logger = logging.getLogger(__name__)
        self._engine = engine

        self._metadata = MetaData(bind=self._engine)
        self._Base = declarative_base()

        self._table_name = table_name
        self._table_schema = table_schema

        self._table = self._reflect_table_metadata()

    @property
    def table(self):
        return self._table

    def create_table(self):
        """ Creates table if table does not exist in database """

        self._logger.debug('Create State %s', self._table)

        if self._table is None:
            table = type('Table', (self._Base, ), self._table_schema)
            table.__table__.create(bind=self._engine)
            self._logger.info('%s table created', self._table_name)

            # update table object after creation
            self._table = self._reflect_table_metadata()

    def drop_table(self):
        """ drops table if exists in database """

        self._logger.debug('Drop State %s', self._table)

        if self._table is not None:
            self._table.drop(self._engine)
            self._logger.info('%s table dropped', self._table_name)
            self._table = self._reflect_table_metadata()

    def insert_data(self, data_dict: list):
        """ Inserts data into table. Data is passed as a list of dictionaries """
        if self._table is None:
            self._logger.error('%s table does not exist. Create table first')
        else:
            conn = self._engine.connect()
            conn.execute(self._table.insert(), data_dict)

    def _reflect_table_metadata(self):
        """ Reflects database object if exists. Returns None if object does no exist """
        self._metadata.clear()
        self._metadata.reflect()
        try:
            table = self._metadata.tables[self._table_name]
        except KeyError:
            table = None
        except Exception as ex:
            self._logger.error(ex)
            raise(ex)

        self._logger.debug(table)
        return table
