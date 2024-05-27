from pathlib import Path
from typing import (
    List,
    Dict,
    Self,
)
from zipfile import ZipFile

from ....ib2d_file.ib2d_file_element import IB2DFileElement
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

    source: Table
    target: Table

    pk_fields: List[FieldPair]
    dt_fields: List[FieldPair]
    fields: List[FieldPair]

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
            working_dir_path=working_dir_path,
        )

        self.description = description

        self.source = source
        self.target = target

        self.pk_fields = pk_fields
        self.dt_fields = dt_fields

    @property
    def fields(
        self,
    ) -> List[FieldPair]:

        return self.pk_fields + self.dt_fields

    @classmethod
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
        source = source_class.deserialize(
            instance_data=source_data,
            working_dir_path=working_dir_path,
            ib2d_file=ib2d_file,
            wildcard_sets=wildcard_sets,
        )

        target_data = instance_data['target']
        target_class = data_sources[target_data['extension_id']]
        target = target_class.deserialize(
            instance_data=target_data,
            working_dir_path=working_dir_path,
            ib2d_file=ib2d_file,
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
            working_dir_path=working_dir_path,
            source=source,
            target=target,
            pk_fields=pk_fields,
            dt_fields=dt_fields,
            description=instance_data['description'],
        )

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
