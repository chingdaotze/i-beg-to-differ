from pathlib import Path
from typing import (
    List,
    Dict,
    Self,
)
from zipfile import ZipFile

from ...ib2d_file.ib2d_file_element import IB2DFileElement
from .table import Table
from .field_pair import FieldPair
from ...wildcards.wildcard_field import WildcardField
from ...wildcards import Wildcards


class Compare(
    IB2DFileElement,
):
    """
    Compare object.
    """

    name: WildcardField
    description: WildcardField

    source: Table
    target: Table

    pk_fields: List[FieldPair]
    dt_fields: List[FieldPair]
    fields: List[FieldPair]

    def __init__(
        self,
        working_dir_path: Path,
        name: str,
        source: Table,
        target: Table,
        wildcards: Wildcards | None = None,
        pk_fields: List[FieldPair] | None = None,
        dt_fields: List[FieldPair] | None = None,
        description: str | None = None,
    ):
        IB2DFileElement.__init__(
            self=self,
            working_dir_path=working_dir_path,
            wildcards=wildcards,
        )

        self.name = WildcardField(
            base_value=name,
            wildcards=self.wildcards,
        )

        self.description = WildcardField(
            base_value=description,
            wildcards=self.wildcards,
        )

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
        wildcards: Wildcards | None = None,
    ) -> Self:

        source = Table.deserialize(
            instance_data=instance_data['source'],
            working_dir_path=working_dir_path,
            ib2d_file=ib2d_file,
            wildcards=wildcards,
        )

        target = Table.deserialize(
            instance_data=instance_data['target'],
            working_dir_path=working_dir_path,
            ib2d_file=ib2d_file,
            wildcards=wildcards,
        )

        pk_fields = [
            FieldPair.deserialize(
                instance_data=pk_field_data,
                working_dir_path=working_dir_path,
                ib2d_file=ib2d_file,
                wildcards=wildcards,
            )
            for pk_field_data in instance_data['pk_fields']
        ]

        dt_fields = [
            FieldPair.deserialize(
                instance_data=dt_field_data,
                working_dir_path=working_dir_path,
                ib2d_file=ib2d_file,
                wildcards=wildcards,
            )
            for dt_field_data in instance_data['dt_fields']
        ]

        instance = Compare(
            working_dir_path=working_dir_path,
            name=instance_data['name'],
            source=source,
            target=target,
            wildcards=wildcards,
            pk_fields=pk_fields,
            dt_fields=dt_fields,
            description=instance_data['description'],
        )

        return instance

    def serialize(
        self,
        ib2d_file: ZipFile,
    ) -> Dict:

        instance_data = {
            'name': self.name.base_value,
            'description': self.description.base_value,
            'source': self.source.serialize(
                ib2d_file=ib2d_file,
            ),
            'target': self.target.serialize(
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

        return instance_data
