from pandas import DataFrame

from ....base import Base
from ....wildcards_sets.wildcard_field import WildcardField
from ....data_sources import DataSources
from ....wildcards_sets import WildcardSets
from ....data_sources.data_source import DataSource
from ....utils.dataframe import dict_to_dataframe


class DataSourceReference(
    Base,
):
    """
    Pointer to a Data Source.
    """

    data_source_name: WildcardField
    """
    Name of the data source.
    """

    data_sources: DataSources
    """
    Global data sources.
    """

    def __init__(
        self,
        data_source_name: str,
        data_sources: DataSources,
        wildcard_sets: WildcardSets | None = None,
    ):

        Base.__init__(
            self=self,
        )

        self.data_source_name = WildcardField(
            base_value=data_source_name,
            wildcard_sets=wildcard_sets,
        )

        self.data_sources = data_sources

    def __str__(
        self,
    ):

        return str(
            self.data_source_name,
        )

    @property
    def data_source(
        self,
    ) -> DataSource:
        """
        Dereferences pointer and provides data source.
        """

        return self.data_sources[
            str(
                self,
            )
        ]

    @property
    def data_types(
        self,
    ) -> DataFrame:
        """
        DataFrame that contains data types.

        - ``column_name``: Name of the column.
        - ``native_type``: Data type recognized by the data source's underlying system.
        - ``py_type``: Data type recognized by Python.
        """

        native_types = dict_to_dataframe(
            data=self.data_source.native_types,
            index='column_name',
            column='native_type',
        )

        data_types = dict_to_dataframe(
            data=self.data_source.py_types,
            index='column_name',
            column='py_type',
        )

        data_types = native_types.join(
            other=data_types,
            how='inner',
        )

        data_types.reset_index(
            inplace=True,
        )

        return data_types
