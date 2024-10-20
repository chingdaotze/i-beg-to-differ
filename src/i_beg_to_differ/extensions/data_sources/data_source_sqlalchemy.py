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
from i_beg_to_differ.core.base import log_exception
from i_beg_to_differ.core.wildcards_sets.wildcard_field import WildcardField
from i_beg_to_differ.core.wildcards_sets import WildcardSets


class DataSourceSqlAlchemy(
    DataSource,
):
    """
    SQLAlchemy file Data Source.
    """

    _drivername: WildcardField
    _table_name: WildcardField
    _username: WildcardField | None
    _password: WildcardField | None
    _host: WildcardField | None
    _port: WildcardField | None
    _database: WildcardField | None
    _query: Dict[WildcardField, WildcardField] | None

    _native_types: Dict[str, str]
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

        self._drivername = WildcardField(
            base_value=drivername,
            wildcard_sets=wildcard_sets,
        )

        self._table_name = WildcardField(
            base_value=table_name,
            wildcard_sets=wildcard_sets,
        )

        if isinstance(username, str):
            self._username = WildcardField(
                base_value=username,
                wildcard_sets=wildcard_sets,
            )

        else:
            self._username = username

        if isinstance(password, str):
            self._password = WildcardField(
                base_value=password,
                wildcard_sets=wildcard_sets,
            )

        else:
            self._password = password

        if isinstance(host, str):
            self._host = WildcardField(
                base_value=host,
                wildcard_sets=wildcard_sets,
            )

        else:
            self._host = host

        if isinstance(port, str):
            self._port = WildcardField(
                base_value=port,
                wildcard_sets=wildcard_sets,
            )

        else:
            self._port = port

        if isinstance(database, str):
            self._database = WildcardField(
                base_value=database,
                wildcard_sets=wildcard_sets,
            )

        else:
            self._database = database

        if isinstance(query, dict):
            self._query = {
                WildcardField(
                    base_value=key,
                    wildcard_sets=wildcard_sets,
                ): WildcardField(
                    base_value=value,
                    wildcard_sets=wildcard_sets,
                )
                for key, value in query.items()
            }

        else:
            self._query = query

        self._native_types = {}

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

        if isinstance(self._username, WildcardField):
            return str(
                self._username,
            )

        else:
            return self._username

    @property
    def password(
        self,
    ) -> str | None:
        """
        SQLAlchemy URL ``password`` parameter.
        More details: https://docs.sqlalchemy.org/en/20/core/engines.html#sqlalchemy.engine.URL
        """

        if isinstance(self._password, WildcardField):
            return str(
                self._password,
            )

        else:
            return self._password

    @property
    def host(
        self,
    ) -> str | None:
        """
        SQLAlchemy URL ``host`` parameter.
        More details: https://docs.sqlalchemy.org/en/20/core/engines.html#sqlalchemy.engine.URL
        """

        if isinstance(self._host, WildcardField):
            return str(
                self._host,
            )

        else:
            return self._host

    @property
    def port(
        self,
    ) -> int | None:
        """
        SQLAlchemy URL ``port`` parameter.
        More details: https://docs.sqlalchemy.org/en/20/core/engines.html#sqlalchemy.engine.URL
        """

        if isinstance(self._port, WildcardField):
            return int(
                self._port,
            )

        else:
            return self._port

    @property
    def database(
        self,
    ) -> str | None:
        """
        SQLAlchemy URL ``database`` parameter.
        More details: https://docs.sqlalchemy.org/en/20/core/engines.html#sqlalchemy.engine.URL
        """

        if isinstance(self._database, WildcardField):
            return str(
                self._database,
            )

        else:
            return self._database

    @property
    def query(
        self,
    ) -> Dict[str, str] | EMPTY_DICT:
        """
        SQLAlchemy URL ``query`` parameter.
        More details: https://docs.sqlalchemy.org/en/20/core/engines.html#sqlalchemy.engine.URL
        """

        if isinstance(self._query, dict):
            return {str(key): str(value) for key, value in self._query.items()}

        elif self._query is None:
            return EMPTY_DICT

        else:
            return self._query

    @property
    def base_url(
        self,
    ) -> URL:
        """
        SQLAlchemy Database URL, without WildCard replacement.
        """

        return URL.create(
            drivername=(
                self._drivername.base_value
                if isinstance(self._drivername, WildcardField)
                else self._drivername
            ),
            username=(
                self._username.base_value
                if isinstance(self._username, WildcardField)
                else self._username
            ),
            password=(
                self._password.base_value
                if isinstance(self._password, WildcardField)
                else self._password
            ),
            host=(
                self._host.base_value
                if isinstance(self._host, WildcardField)
                else self._host
            ),
            port=(
                self._port.base_value
                if isinstance(self._port, WildcardField)
                else self._port
            ),
            database=(
                self._database.base_value
                if isinstance(self._database, WildcardField)
                else self._database
            ),
            query=(
                {key.base_value: value.base_value for key, value in self._query.items()}
                if isinstance(self._query, dict)
                else self._query
            ),
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

        # https://docs.sqlalchemy.org/en/20/core/reflection.html
        table = Table(
            self.table_name,
            MetaData(),
            autoload_with=engine,
        )

        self._native_types = {column.name: str(column.type) for column in table.columns}

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
            'description': self.description,
            'parameters': {
                'drivername': self._drivername,
                'table_name': self._table_name,
                'username': self._username,
                'password': self._password,
                'host': self._host,
                'database': self._database,
                'query': self._query,
            },
        }

    @property
    def native_types(
        self,
    ) -> Dict[str, str]:

        return self._native_types