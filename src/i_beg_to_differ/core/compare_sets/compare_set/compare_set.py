from typing import (
    List,
    Dict,
    Self,
)
from pathlib import Path
from zipfile import ZipFile

from ...ib2d_file.ib2d_file_element import IB2DFileElement
from ...base import log_exception
from .compare import Compare
from ...wildcards_sets import WildcardSets
from ...data_sources import DataSources


class CompareSet(
    IB2DFileElement,
):
    """
    Compare set object. Contains a collection of compares.
    """

    name: str
    """
    Unique name for this Compare Set.
    """

    description: str | None
    """
    Human-readable description of this Compare Set.
    """

    _compares: List[Compare]

    def __init__(
        self,
        name: str,
        description: str | None = None,
        compares: List[Compare] | None = None,
    ):
        IB2DFileElement.__init__(
            self=self,
        )

        self.name = name

        if description is None:
            description = ''

        self.description = description

        if compares is None:
            compares = []

        self._compares = compares

    def __str__(
        self,
    ) -> str:

        return self.name

    def __getitem__(
        self,
        key: str | Compare,
    ) -> Compare:

        key = str(
            key,
        )

        return self.compares[key]

    @property
    def compares(
        self,
    ) -> Dict[str, Compare]:

        return {str(compare): compare for compare in self._compares}

    def append(
        self,
        compare: Compare,
    ) -> None:
        """
        Add compare to the collection of compares.

        :param compare: Compare set to add.
        :return:
        """

        if compare not in self._compares:
            self._compares.append(
                compare,
            )

    @classmethod
    @log_exception
    def deserialize(
        cls,
        instance_data: Dict,
        working_dir_path: Path,
        ib2d_file: ZipFile,
        data_sources: DataSources = None,
        wildcard_sets: WildcardSets | None = None,
    ) -> Self:

        for name, compare_values in instance_data['compares'].items():
            compare_values['name'] = name

        return CompareSet(
            name=instance_data['name'],
            description=instance_data['description'],
            compares=[
                Compare.deserialize(
                    instance_data=compare_values,
                    working_dir_path=working_dir_path,
                    ib2d_file=ib2d_file,
                    data_sources=data_sources,
                    wildcard_sets=wildcard_sets,
                )
                for compare_values in instance_data['compares'].values()
            ],
        )

    @log_exception
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

    def to_parquet(
        self,
        dir_path: Path | str,
        file_name_prefix: str | None = None,
    ) -> None:

        if file_name_prefix is None:
            file_name_prefix = ''

        for compare in self._compares:

            compare.to_parquet(
                dir_path=dir_path,
                file_name_prefix=f'{file_name_prefix}{str(compare)}_',
            )

    def to_csv(
        self,
        dir_path: Path | str,
        file_name_prefix: str | None = None,
    ) -> None:

        if file_name_prefix is None:
            file_name_prefix = ''

        for compare in self._compares:

            compare.to_csv(
                dir_path=dir_path,
                file_name_prefix=f'{file_name_prefix}{str(compare)}_',
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

        for compare in self._compares:

            path = dir_path / f'{file_name_prefix}{str(compare)}.xlsx'

            compare.to_excel(
                path=path,
            )
