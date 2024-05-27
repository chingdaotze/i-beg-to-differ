from typing import (
    Dict,
    Self,
)
from pathlib import Path
from zipfile import ZipFile

from ..ib2d_file.ib2d_file_element import IB2DFileElement
from .compare_set import CompareSet
from ..wildcards_sets import WildcardSets


class CompareSets(
    IB2DFileElement,
):
    """
    Compare set object. Contains a collection of compares.
    """

    compare_sets: Dict[str, CompareSet] | None
    _DEFAULT_COMPARE_SET = 'Default'

    def __init__(
        self,
        working_dir_path: Path,
        compare_sets: Dict[str, CompareSet] | None = None,
    ):
        IB2DFileElement.__init__(
            self=self,
            working_dir_path=working_dir_path,
        )

        self.compare_sets = compare_sets

    @classmethod
    def deserialize(
        cls,
        instance_data: Dict,
        working_dir_path: Path,
        ib2d_file: ZipFile,
        wildcard_sets: WildcardSets | None = None,
    ) -> Self:

        return CompareSets(
            working_dir_path=working_dir_path,
            compare_sets={
                name: CompareSet.deserialize(
                    instance_data=compare_set_values,
                    working_dir_path=working_dir_path,
                    ib2d_file=ib2d_file,
                    wildcard_sets=wildcard_sets,
                )
                for name, compare_set_values in instance_data.items()
            },
        )

    def serialize(
        self,
        ib2d_file: ZipFile,
    ) -> Dict:

        return {
            name: instance.serialize(
                ib2d_file=ib2d_file,
            )
            for name, instance in self.compare_sets.items()
        }
