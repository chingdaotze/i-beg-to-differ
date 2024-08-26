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

    compare_sets: Dict[str, CompareSet] | None
    _DEFAULT_COMPARE_SET = 'Default'

    def __init__(
        self,
        compare_sets: Dict[str, CompareSet] | None = None,
    ):
        IB2DFileElement.__init__(
            self=self,
        )

        self.compare_sets = compare_sets

    def __str__(
        self,
    ) -> str:

        if isinstance(self.compare_sets, dict):
            return str(
                [compare_set_name for compare_set_name in self.compare_sets.keys()],
            )

        else:
            return str(
                self.compare_sets,
            )

    @log_exception
    def __setitem__(
        self,
        key: str,
        value: CompareSet,
    ) -> None:
        if self.compare_sets is None:
            self.compare_sets = {}

        if not isinstance(self.compare_sets, dict):
            raise TypeError(
                'CompareSets collection is not a dictionary!',
            )

        self.compare_sets[key] = value

    @log_exception
    def __getitem__(
        self,
        item: str,
    ) -> CompareSet:

        if self.compare_sets is None:
            raise ValueError(
                'CompareSets object is empty!',
            )

        if not isinstance(self.compare_sets, dict):
            raise TypeError(
                'CompareSets collection is not a dictionary!',
            )

        return self.compare_sets[item]

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

        return CompareSets(
            compare_sets={
                name: CompareSet.deserialize(
                    instance_data=compare_set_values,
                    working_dir_path=working_dir_path,
                    ib2d_file=ib2d_file,
                    data_sources=data_sources,
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
