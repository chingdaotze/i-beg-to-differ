from typing import (
    Dict,
    Self,
)
from pathlib import Path
from zipfile import ZipFile

from ...ib2d_file.ib2d_file_element import IB2DFileElement
from .compare import Compare
from ...wildcards_sets import WildcardSets


class CompareSet(
    IB2DFileElement,
):
    """
    Compare set object. Contains a collection of compares.
    """

    description: str | None
    """
    Human-readable description of this Compare Set.
    """

    compares: Dict[str, Compare] | None
    """
    Collection of Compare objects.
    """

    def __init__(
        self,
        working_dir_path: Path,
        description: str | None = None,
        compares: Dict[str, Compare] | None = None,
    ):
        IB2DFileElement.__init__(
            self=self,
            working_dir_path=working_dir_path,
        )

        self.description = description
        self.compares = compares

    @classmethod
    def deserialize(
        cls,
        instance_data: Dict,
        working_dir_path: Path,
        ib2d_file: ZipFile,
        wildcard_sets: WildcardSets | None = None,
    ) -> Self:

        return CompareSet(
            working_dir_path=working_dir_path,
            description=instance_data['description'],
            compares={
                name: Compare.deserialize(
                    instance_data=compare_set_values,
                    working_dir_path=working_dir_path,
                    ib2d_file=ib2d_file,
                    wildcard_sets=wildcard_sets,
                )
                for name, compare_set_values in instance_data['compares'].items()
            },
        )

    def serialize(
        self,
        ib2d_file: ZipFile,
    ) -> Dict:

        return {
            'description': self.description,
            'compares': {
                name: instance.serialize(
                    ib2d_file=ib2d_file,
                )
                for name, instance in self.compares.items()
            },
        }
