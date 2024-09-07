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
from .....base import log_exception
from .....wildcards_sets import WildcardSets
from .....data_sources.data_source import DataSource
from .....utils.dataframe import dict_to_dataframe
from .....extensions.data_sources.data_source_dataframe import DataSourceDataFrame
from .....compare_engine import CompareEngine
from .....compare_sets.compare_set.compare.field_pair import FieldPair


class DataSourcePair(
    IB2DFileElement,
):
    """
    Pair of data sources for comparison. Functions as a pointer to underlying
    Data Sources.
    """

    data_sources: DataSources

    source: str
    """
    Pointer to source data source.
    """

    target: str
    """
    Pointer to target data source.
    """

    def __init__(
        self,
        data_sources: DataSources,
        source: str,
        target: str,
    ):
        IB2DFileElement.__init__(
            self=self,
        )

        self.data_sources = data_sources
        self.source = source
        self.target = target

    def __str__(
        self,
    ) -> str:

        return f'{self.source} | {self.target}'

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
        )

    @log_exception
    def serialize(
        self,
        ib2d_file: ZipFile,
    ) -> Dict:

        return {
            'source': self.source,
            'target': self.target,
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

        return types

    @cached_property
    def schema_comparison(
        self,
    ) -> DataFrame:

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
                FieldPair(
                    source_field='column',
                    target_field='column',
                ),
            ],
            dt_fields=[
                FieldPair(
                    source_field='native_type',
                    target_field='native_type',
                ),
                FieldPair(
                    source_field='py_type',
                    target_field='py_type',
                ),
            ],
        )

        values_comparison = compare_engine.values_comparison
