from pathlib import Path
from typing import (
    Dict,
    Self,
)
from zipfile import ZipFile
from functools import cached_property

from pandas import DataFrame

from .....ib2d_file.ib2d_file_element import IB2DFileElement
from .....data_sources import DataSources
from .....input_fields.wildcard_input_fields import WildcardInputField
from .data_source_options import DataSourceOptions
from .....base import log_exception
from .....wildcards_sets import WildcardSets
from .....data_sources.data_source import DataSource
from .....utils.dataframe import dict_to_dataframe
from i_beg_to_differ.extensions.data_sources.data_source_dataframe import (
    DataSourceDataFrame,
)
from .....compare_engine import (
    CompareEngine,
    AUTO_MATCH,
)
from .....compare_sets.compare_set.compare.field_pair import FieldPairPrimaryKey


class DataSourcePair(
    IB2DFileElement,
):
    """
    Pair of data sources for comparison. Functions as a pointer to underlying
    Data Sources.
    """

    data_sources: DataSources
    source_input_field: WildcardInputField
    target_input_field: WildcardInputField

    def __init__(
        self,
        data_sources: DataSources,
        source: str,
        target: str,
        wildcard_sets: WildcardSets | None = None,
    ):
        IB2DFileElement.__init__(
            self=self,
        )

        self.data_sources = data_sources

        options = DataSourceOptions(
            data_sources=self.data_sources,
        )

        self.source_input_field = WildcardInputField(
            base_value=source,
            title='Source',
            wildcard_sets=wildcard_sets,
            options=options,
        )

        self.target_input_field = WildcardInputField(
            base_value=target,
            title='Target',
            wildcard_sets=wildcard_sets,
            options=options,
        )

    def __str__(
        self,
    ) -> str:

        return f'{self.source} | {self.target}'

    @property
    def source(
        self,
    ) -> str:
        """
        Pointer to source data source.
        """

        return str(
            self.source_input_field,
        )

    @property
    def target(
        self,
    ) -> str:
        """
        Pointer to target data source.
        """

        return str(
            self.target_input_field,
        )

    @classmethod
    @log_exception
    def deserialize(
        cls,
        instance_data: Dict,
        working_dir_path: Path,
        ib2d_file: ZipFile,
        data_sources: DataSources,
        wildcard_sets: WildcardSets | None = None,
    ) -> Self:

        return DataSourcePair(
            data_sources=data_sources,
            source=instance_data['source'],
            target=instance_data['target'],
            wildcard_sets=wildcard_sets,
        )

    @log_exception
    def serialize(
        self,
        ib2d_file: ZipFile,
    ) -> Dict:

        return {
            'source': self.source_input_field.base_value,
            'target': self.target_input_field.base_value,
        }

    def init_caches(
        self,
    ) -> None:
        """
        Initializes caches for this instance. More performant than lazy loading,
        as it performs cache initialization in parallel.

        :return:
        """

        self.data_sources.init_caches(
            data_sources=[
                self.source,
                self.target,
            ]
        )

    @staticmethod
    def types_to_dataframe(
        data_source: DataSource,
    ) -> DataFrame:
        """
        Creates a DataFrame that contains both source and target data types.

        - ``column_name``: Name of the column.
        - ``native_type``: Data type recognized by the data source's underlying system.
        - ``py_type``: Data type recognized by Python.

        :param data_source: Data source to parse.
        :return:
        """

        native_types = dict_to_dataframe(
            data=data_source.native_types,
            index='column_name',
            column='native_type',
        )

        py_types = dict_to_dataframe(
            data=data_source.py_types,
            index='column_name',
            column='py_type',
        )

        types = native_types.join(
            other=py_types,
            how='inner',
        )

        types.reset_index(
            inplace=True,
        )

        return types

    @cached_property
    def schema_comparison(
        self,
    ) -> DataFrame:
        """
        Schema comparison between source and target data sources.

        - ``src.[column_name] | tgt.[column_name]``: Name of the column.
        - ``src.[native_type]``: Source data type recognized by the data source's underlying system.
        - ``tgt.[native_type]``: Target data type recognized by the data source's underlying system.
        - ``src.[py_type]``: Source data type recognized by Python.
        - ``tgt.[py_type]``: Target data type recognized by Python.

        :return:
        """

        self.init_caches()

        source_types = self.types_to_dataframe(
            data_source=self.data_sources[self.source],
        )

        target_types = self.types_to_dataframe(
            data_source=self.data_sources[self.target],
        )

        source_types = DataSourceDataFrame(
            data=source_types,
        )

        target_types = DataSourceDataFrame(
            data=target_types,
        )

        data_sources = DataSources(
            data_sources={
                'source': source_types,
                'target': target_types,
            }
        )

        compare_engine = CompareEngine(
            data_sources=data_sources,
            source='source',
            target='target',
            pk_fields=[
                FieldPairPrimaryKey(
                    source_field='column_name',
                    target_field='column_name',
                ),
            ],
            dt_fields=AUTO_MATCH,
        )

        return compare_engine.values_comparison
