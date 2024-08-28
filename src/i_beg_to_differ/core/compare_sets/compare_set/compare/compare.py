from pathlib import Path
from typing import (
    Callable,
    List,
    Dict,
    Self,
)
from zipfile import ZipFile

from ....ib2d_file.ib2d_file_element import IB2DFileElement
from ....compare_engine import CompareEngine
from .data_source_pair import DataSourcePair
from .field_pair import FieldPair
from ....base import log_exception
from ....data_sources import DataSources
from ....wildcards_sets import WildcardSets


class Compare(
    IB2DFileElement,
    CompareEngine,
):
    """
    Compare object.
    """

    description: str | None
    """
    Human-readable description.
    """

    data_source_pair: DataSourcePair
    """
    Data source pair.
    """

    init_caches: Callable
    """
    Convenience stub to underlying data_sources.init_caches.
    """

    def __init__(
        self,
        data_sources: DataSources,
        data_source_pair: DataSourcePair,
        pk_fields: List[FieldPair] | None = None,
        dt_fields: List[FieldPair] | None = None,
        description: str | None = None,
    ):
        IB2DFileElement.__init__(
            self=self,
        )

        CompareEngine.__init__(
            self=self,
            data_sources=data_sources,
            source=data_source_pair.source,
            target=data_source_pair.target,
            pk_fields=pk_fields,
            dt_fields=dt_fields,
        )

        self.description = description
        self.data_source_pair = data_source_pair
        self.init_caches = self.data_sources.init_caches

    def __str__(
        self,
    ) -> str:
        # TODO: Implement hash to make this unique

        return str(
            self.data_source_pair,
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

        data_source_pair = DataSourcePair.deserialize(
            instance_data=instance_data,
            working_dir_path=working_dir_path,
            ib2d_file=ib2d_file,
            data_sources=data_sources,
            wildcard_sets=wildcard_sets,
        )

        pk_fields = [
            FieldPair.deserialize(
                instance_data=pk_field_data,
                working_dir_path=working_dir_path,
                ib2d_file=ib2d_file,
                wildcard_sets=wildcard_sets,
            )
            for pk_field_data in instance_data['pk_fields']
        ]

        dt_fields = [
            FieldPair.deserialize(
                instance_data=dt_field_data,
                working_dir_path=working_dir_path,
                ib2d_file=ib2d_file,
                wildcard_sets=wildcard_sets,
            )
            for dt_field_data in instance_data['dt_fields']
        ]

        return Compare(
            data_sources=data_sources,
            data_source_pair=data_source_pair,
            pk_fields=pk_fields,
            dt_fields=dt_fields,
            description=instance_data['description'],
        )

    @log_exception
    def serialize(
        self,
        ib2d_file: ZipFile,
    ) -> Dict:

        return {
            'description': self.description,
            'source': self.source,
            'target': self.target,
            'pk_fields': [
                instance.serialize(
                    ib2d_file=ib2d_file,
                )
                for instance in self.pk_fields
            ],
            'dt_fields': [
                instance.serialize(
                    ib2d_file=ib2d_file,
                )
                for instance in self.dt_fields
            ],
        }
