from pathlib import Path
from typing import (
    Dict,
    Self,
)
from zipfile import ZipFile
from functools import cached_property

from pandas import DataFrame

from .....ib2d_file.ib2d_file_element import IB2DFileElement
from .....compare_engine import CompareEngine
from .....data_sources.data_source import DataSource
from .....data_sources import DataSources
from .....compare_sets.compare_set.compare.field_pair import FieldPair
from .....base import log_exception
from .....wildcards_sets import WildcardSets
from .....utils.dataframe import dict_to_dataframe


class DataSourcePair(
    IB2DFileElement,
    CompareEngine,
):
    source: DataSource
    """
    Source data source object.
    """

    target: DataSource
    """
    Target data source object.
    """

    _data_sources: DataSources
    """
    All data sources.
    """

    def __init__(
        self,
        source: DataSource,
        target: DataSource,
        data_sources: DataSources,
    ):
        IB2DFileElement.__init__(
            self=self,
        )

        CompareEngine.__init__(
            self=self,
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

        self.source = source
        self.target = target
        self._data_sources = data_sources

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

        source_data_source_id = instance_data['source']
        source = data_sources[source_data_source_id]

        target_data_source_id = instance_data['target']
        target = data_sources[target_data_source_id]

        return DataSourcePair(
            source=source,
            target=target,
            data_sources=data_sources,
        )

    @log_exception
    def serialize(
        self,
        ib2d_file: ZipFile,
    ) -> Dict:

        return {
            'source': self.source.serialize(
                ib2d_file=ib2d_file,
            ),
            'target': self.source.serialize(
                ib2d_file=ib2d_file,
            ),
        }

    @cached_property
    def src_df(
        self,
    ) -> DataFrame:
        self.init_caches()

        return self.types_to_dataframe(
            data_source=self.source,
        )

    @cached_property
    def tgt_df(
        self,
    ) -> DataFrame:
        self.init_caches()

        return self.types_to_dataframe(
            data_source=self.target,
        )

    def init_caches(
        self,
    ) -> None:
        self._data_sources.init_caches(
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

        source_types = self.src_df
        target_types = self.tgt_df

        pass
