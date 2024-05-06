from pathlib import Path
from typing import (
    List,
    Dict,
    Self,
)
from zipfile import ZipFile

from ...ib2d_file.ib2d_file_element import IB2DFileElement
from ...data_sources.data_source import DataSource
from .field_pair import FieldPair
from ...wildcards import Wildcards


class Compare(
    IB2DFileElement,
):
    """
    Compare object.
    """

    name: str
    description: str

    source: DataSource
    target: DataSource

    pk_fields: List[FieldPair]
    dt_fields: List[FieldPair]
    fields: List[FieldPair]

    def __init__(
        self,
        working_dir_path: Path,
        name: str,
        source: DataSource,
        target: DataSource,
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

        self.name = name
        self.description = description

        self.source = source
        self.target = target

        self.pk_fields = pk_fields
        self.dt_fields = dt_fields
        self.fields = self.pk_fields + self.dt_fields

    @classmethod
    def deserialize(
        cls,
        instance_data: Dict,
        working_dir_path: Path,
        ib2d_file: ZipFile,
    ) -> Self:

        # TODO: Deserialize object

        pass
