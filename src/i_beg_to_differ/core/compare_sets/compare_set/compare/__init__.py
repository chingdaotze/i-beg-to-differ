from pathlib import Path
from typing import (
    List,
    Dict,
    Self,
)
from zipfile import ZipFile

from ....ib2d_file.ib2d_file_element import IB2DFileElement
from ....base import (
    log_exception,
    log_runtime,
)
from .table import Table
from .field_pair import FieldPair
from ....wildcards_sets import WildcardSets
from ....extensions.data_sources import DataSources


class Compare(
    IB2DFileElement,
):
    """
    Compare object.
    """

    description: str | None
    """
    Human-readable description.
    """

    source: Table
    """
    Source table object.
    """

    target: Table
    """
    Target table object.
    """

    pk_fields: List[FieldPair]
    """
    Primary key field pairs.
    """

    dt_fields: List[FieldPair]
    """
    Data field pairs.
    """

    fields: List[FieldPair]
    """
    All field pairs.
    """

    def __init__(
        self,
        working_dir_path: Path,
        source: Table,
        target: Table,
        pk_fields: List[FieldPair] | None = None,
        dt_fields: List[FieldPair] | None = None,
        description: str | None = None,
    ):
        IB2DFileElement.__init__(
            self=self,
            module_name=__name__,
            working_dir_path=working_dir_path,
        )

        self.description = description

        self.source = source
        self.target = target

        self.pk_fields = pk_fields
        self.dt_fields = dt_fields

    def __str__(
        self,
    ) -> str:

        return f'{self.source} | {self.target}'

    @log_exception
    @log_runtime
    def load(
        self,
    ) -> None:
        source_df = self.pool.apply_async(
            func=self.source.data_source.load,
        )

        target_df = self.pool.apply_async(
            func=self.target.data_source.load
        )

        self.source.data = source_df.get()
        self.target.data = target_df.get()

    @property
    def fields(
        self,
    ) -> List[FieldPair]:

        return self.pk_fields + self.dt_fields

    @classmethod
    @log_exception
    def deserialize(
        cls,
        instance_data: Dict,
        working_dir_path: Path,
        ib2d_file: ZipFile,
        wildcard_sets: WildcardSets | None = None,
    ) -> Self:

        data_sources = DataSources()

        source_data = instance_data['source']
        source_class = data_sources[source_data['extension_id']]
        source_data_source = source_class.deserialize(
            instance_data=source_data,
            working_dir_path=working_dir_path,
            ib2d_file=ib2d_file,
            wildcard_sets=wildcard_sets,
        )
        source = Table(
            data_source=source_data_source,
        )

        target_data = instance_data['target']
        target_class = data_sources[target_data['extension_id']]
        target_data_source = target_class.deserialize(
            instance_data=target_data,
            working_dir_path=working_dir_path,
            ib2d_file=ib2d_file,
            wildcard_sets=wildcard_sets,
        )
        target = Table(
            data_source=target_data_source,
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
            working_dir_path=working_dir_path,
            source=source,
            target=target,
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
            'source': self.source.data_source.serialize(
                ib2d_file=ib2d_file,
            ),
            'target': self.source.data_source.serialize(
                ib2d_file=ib2d_file,
            ),
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
