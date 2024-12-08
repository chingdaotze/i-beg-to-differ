from typing import (
    List,
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

    _compare_sets: List[CompareSet]

    def __init__(
        self,
        compare_sets: List[CompareSet] | None = None,
    ):
        IB2DFileElement.__init__(
            self=self,
        )

        if compare_sets is None:
            compare_sets = []

        self._compare_sets = compare_sets

    def __str__(
        self,
    ) -> str:

        return 'Compare Sets'

    def __getitem__(
        self,
        compare_set: str | CompareSet,
    ) -> CompareSet:

        key = str(
            compare_set,
        )

        return self.compare_sets[key]

    @property
    def compare_sets(
        self,
    ) -> Dict[str, CompareSet]:

        return {str(compare_set): compare_set for compare_set in self._compare_sets}

    def append(
        self,
        compare_set: CompareSet,
    ):
        """
        Add compare set to the collection of compare sets.

        :param compare_set: Compare set to add.
        :return:
        """

        if compare_set not in self._compare_sets:
            self._compare_sets.append(
                compare_set,
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

        for name, compare_set_values in instance_data.items():
            compare_set_values['name'] = name

        return CompareSets(
            compare_sets=[
                CompareSet.deserialize(
                    instance_data=compare_set_values,
                    working_dir_path=working_dir_path,
                    ib2d_file=ib2d_file,
                    data_sources=data_sources,
                    wildcard_sets=wildcard_sets,
                )
                for compare_set_values in instance_data.values()
            ],
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

    def to_parquet(
        self,
        dir_path: Path | str,
        file_name_prefix: str | None = None,
    ) -> None:

        if file_name_prefix is None:
            file_name_prefix = ''

        for compare_set in self._compare_sets:

            compare_set.to_parquet(
                dir_path=dir_path,
                file_name_prefix=f'{file_name_prefix}{str(compare_set)}_',
            )

    def to_csv(
        self,
        dir_path: Path | str,
        file_name_prefix: str | None = None,
    ) -> None:

        if file_name_prefix is None:
            file_name_prefix = ''

        for compare_set in self._compare_sets:

            compare_set.to_csv(
                dir_path=dir_path,
                file_name_prefix=f'{file_name_prefix}{str(compare_set)}_',
            )

    def to_excel(
        self,
        dir_path: Path | str,
        file_name_prefix: str | None = None,
    ) -> None:

        if file_name_prefix is None:
            file_name_prefix = ''

        if isinstance(dir_path, str):
            dir_path = Path(
                dir_path,
            )

        for compare_set in self._compare_sets:

            compare_set.to_excel(
                dir_path=dir_path,
                file_name_prefix=f'{file_name_prefix}{str(compare_set)}_',
            )
