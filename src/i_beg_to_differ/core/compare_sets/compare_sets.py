from typing import (
    Dict,
    Self,
)
from pathlib import Path
from zipfile import ZipFile

from ..ib2d_file.ib2d_file_element import IB2DFileElement
from ..base import log_exception
from .compare_set import CompareSet
from ..data_sources import DataSources
from ..wildcards_sets import WildcardSets


class CompareSets(
    IB2DFileElement,
):
    """
    Compare set object. Contains a collection of compares.
    """

    compare_sets: Dict[str, CompareSet]
    _DEFAULT_COMPARE_SET = 'Default'

    def __init__(
        self,
        compare_sets: Dict[str, CompareSet] | None = None,
    ):
        IB2DFileElement.__init__(
            self=self,
        )

        if compare_sets is None:
            compare_sets = {}

        self.compare_sets = compare_sets

    def __str__(
        self,
    ) -> str:

        return 'Compare Sets'

    @log_exception
    def __setitem__(
        self,
        key: str,
        value: CompareSet,
    ) -> None:

        self.compare_sets[key] = value

    @log_exception
    def __getitem__(
        self,
        item: str,
    ) -> CompareSet:

        return self.compare_sets[item]

    def set_data_sources(
        self,
        data_sources: DataSources,
    ) -> None:

        for compare_set in self.compare_sets.values():
            compare_set.set_data_sources(
                data_sources=data_sources,
            )

    @classmethod
    @log_exception
    def deserialize(
        cls,
        instance_data: Dict,
        working_dir_path: Path,
        ib2d_file: ZipFile,
        wildcard_sets: WildcardSets | None = None,
    ) -> Self:

        return CompareSets(
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

    @log_exception
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
