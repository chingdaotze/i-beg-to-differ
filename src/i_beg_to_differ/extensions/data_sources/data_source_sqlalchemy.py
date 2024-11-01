from pathlib import Path
from typing import (
    Dict,
    Self,
)
from zipfile import ZipFile

from sqlalchemy import (
    URL,
    create_engine,
    Table,
    MetaData,
)
from sqlalchemy.util import EMPTY_DICT
from pandas import read_sql

from i_beg_to_differ.core.data_sources.data_source import DataSource
from i_beg_to_differ.core.extensions.input_fields import (
    WildcardInputField,
    DictInputField,
)
from i_beg_to_differ.core.base import log_exception
from i_beg_to_differ.core.wildcards_sets import WildcardSets


class DataSourceSqlAlchemy(
    DataSource,
):
    """
    SQLAlchemy file Data Source.
    """

    _drivername: WildcardInputField
    _table_name: WildcardInputField
    _username: WildcardInputField
    _password: WildcardInputField
    _host: WildcardInputField
    _port: WildcardInputField
    _database: WildcardInputField
    _query: DictInputField

    extension_name = 'SQLAlchemy Connection'

    def __init__(
        self,
        drivername: str,
        table_name: str,
        username: str | None = None,
        password: str | None = None,
        host: str | None = None,
        port: int | str | None = None,
        database: str | None = None,
        query: Dict[str, str] | None = None,
        description: str | None = None,
        wildcard_sets: WildcardSets | None = None,
    ):

        DataSource.__init__(
            self=self,
            description=description,
        )

        self._drivername = WildcardInputField(
            label='Driver Name: ',
            base_value=drivername,
            wildcard_sets=wildcard_sets,
        )

        self._table_name = WildcardInputField(
            label='Table Name: ',
            base_value=table_name,
            wildcard_sets=wildcard_sets,
        )

        if not isinstance(username, str):
            username = ''

        self._username = WildcardInputField(
            label='Username: ',
            base_value=username,
            wildcard_sets=wildcard_sets,
        )

        if not isinstance(password, str):
            password = ''

        self._password = WildcardInputField(
            label='Password: ',
            base_value=password,
            wildcard_sets=wildcard_sets,
        )

        if not isinstance(host, str):
            host = ''

        self._host = WildcardInputField(
            label='Host: ',
            base_value=host,
            wildcard_sets=wildcard_sets,
        )

        if not isinstance(port, str):
            port = ''

        self._port = WildcardInputField(
            label='Port: ',
            base_value=port,
            wildcard_sets=wildcard_sets,
        )

        if not isinstance(database, str):
            database = ''

        self._database = WildcardInputField(
            label='Database: ',
            base_value=database,
            wildcard_sets=wildcard_sets,
        )

        if not isinstance(query, dict):
            query = {}

        self._query = DictInputField(
            label='Query: ',
            values=query,
            wildcard_sets=wildcard_sets,
        )

    def __str__(
        self,
    ) -> str:

        return f'{self.extension_name}: \'{self.base_url}\', Table: \'{self._table_name.base_value}\''

    @property
    def drivername(
        self,
    ) -> str:
        """
        SQLAlchemy URL ``drivername`` parameter.
        More details: https://docs.sqlalchemy.org/en/20/core/engines.html#sqlalchemy.engine.URL
        """

        return str(
            self._drivername,
        )

    @property
    def table_name(
        self,
    ) -> str:
        """
        SQLAlchemy Table ``name`` parameter.
        More details: https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table.params.name
        """

        return str(
            self._table_name,
        )

    @property
    def username(
        self,
    ) -> str | None:
        """
        SQLAlchemy URL ``username`` parameter.
        More details: https://docs.sqlalchemy.org/en/20/core/engines.html#sqlalchemy.engine.URL
        """

        username = str(
            self._username,
        )

        if not username:
            username = None

        return username

    @property
    def password(
        self,
    ) -> str | None:
        """
        SQLAlchemy URL ``password`` parameter.
        More details: https://docs.sqlalchemy.org/en/20/core/engines.html#sqlalchemy.engine.URL
        """

        password = str(self._password)

        if not password:
            password = None

        return password

    @property
    def host(
        self,
    ) -> str | None:
        """
        SQLAlchemy URL ``host`` parameter.
        More details: https://docs.sqlalchemy.org/en/20/core/engines.html#sqlalchemy.engine.URL
        """

        host = str(self._host)

        if not host:
            host = None

        return host

    @property
    def port(
        self,
    ) -> int | None:
        """
        SQLAlchemy URL ``port`` parameter.
        More details: https://docs.sqlalchemy.org/en/20/core/engines.html#sqlalchemy.engine.URL
        """

        port = str(
            self._port,
        )

        if port:
            port = int(
                port,
            )

        else:
            port = None

        return port

    @property
    def database(
        self,
    ) -> str | None:
        """
        SQLAlchemy URL ``database`` parameter.
        More details: https://docs.sqlalchemy.org/en/20/core/engines.html#sqlalchemy.engine.URL
        """

        database = str(
            self._database,
        )

        if not database:
            database = None

        return database

    @property
    def query(
        self,
    ) -> Dict[str, str] | EMPTY_DICT:
        """
        SQLAlchemy URL ``query`` parameter.
        More details: https://docs.sqlalchemy.org/en/20/core/engines.html#sqlalchemy.engine.URL
        """

        if self._query:
            return {str(key): str(value) for key, value in self._query.values.items()}

        else:
            return EMPTY_DICT

    @property
    def base_url(
        self,
    ) -> URL:
        """
        SQLAlchemy Database URL, without WildCard replacement.
        """

        return URL.create(
            drivername=self._drivername.base_value,
            username=self._username.base_value,
            password=self._password.base_value,
            host=self._host.base_value,
            port=self.port,
            database=self._database.base_value,
            query={
                key.base_value: value.base_value
                for key, value in self._query.values.items()
            },
        )

    @property
    def url(
        self,
    ) -> URL:
        """
        SQLAlchemy Database URL.
        More details: https://docs.sqlalchemy.org/en/20/core/engines.html#database-urls
        """

        return URL.create(
            drivername=self.drivername,
            username=self.username,
            password=self.password,
            host=self.host,
            port=self.port,
            database=self.database,
            query=self.query,
        )

    def load(
        self,
    ) -> Self:
        self.log_info(
            msg=f'Loading data from URL: {self.url} ...',
        )

        engine = create_engine(
            url=self.url,
        )

        table = Table(
            self.table_name,
            MetaData(),
            autoload_with=engine,
        )

        sql = str(table.select())

        self.log_info(msg=f'Loading table using query:\n\n{sql}')

        self.cache = read_sql(
            sql=sql,
            con=engine,
        )

        return self

    @classmethod
    @log_exception
    def deserialize(
        cls,
        instance_data: Dict,
        working_dir_path: Path,
        ib2d_file: ZipFile,
        wildcard_sets: WildcardSets | None = None,
    ) -> Self:

        return DataSourceSqlAlchemy(
            drivername=instance_data['parameters']['drivername'],
            table_name=instance_data['parameters']['table_name'],
            username=instance_data['parameters']['username'],
            password=instance_data['parameters']['password'],
            host=instance_data['parameters']['host'],
            database=instance_data['parameters']['database'],
            query=instance_data['parameters']['query'],
            wildcard_sets=wildcard_sets,
        )

    @log_exception
    def serialize(
        self,
        ib2d_file: ZipFile,
    ) -> Dict:

        return {
            'extension_id': self.get_extension_id(),
            'description': self.description.value,
            'parameters': {
                'drivername': self._drivername.base_value,
                'table_name': self._table_name.base_value,
                'username': self._username.base_value,
                'password': self._password.base_value,
                'host': self._host.base_value,
                'database': self._database.base_value,
                'query': {
                    key.base_value: value.base_value
                    for key, value in self._query.values.items()
                },
            },
        }

    @property
    def native_types(
        self,
    ) -> Dict[str, str]:

        engine = create_engine(
            url=self.url,
        )

        # https://docs.sqlalchemy.org/en/20/core/reflection.html
        table = Table(
            self.table_name,
            MetaData(),
            autoload_with=engine,
        )

        return {column.name: str(column.type) for column in table.columns}
