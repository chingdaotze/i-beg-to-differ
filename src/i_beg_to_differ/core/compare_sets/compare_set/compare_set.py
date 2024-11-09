from typing import (
    Dict,
    Self,
)
from pathlib import Path
from zipfile import ZipFile

from ...ib2d_file.ib2d_file_element import IB2DFileElement
from ...base import (
    log_exception,
    log_runtime,
)
from ...input_fields import TextBoxInputField
from .compare import Compare
from ...wildcards_sets import WildcardSets
from ...data_sources import DataSources


class CompareSet(
    IB2DFileElement,
):
    """
    Compare set object. Contains a collection of compares.
    """

    description: TextBoxInputField
    """
    Human-readable description of this Compare Set.
    """

    compares: Dict[str, Compare] | None
    """
    Collection of Compare objects.
    """

    def __init__(
        self,
        description: str | None = None,
        compares: Dict[str, Compare] | None = None,
    ):
        IB2DFileElement.__init__(
            self=self,
        )

        self.description = TextBoxInputField(
            title='Description',
            value=description,
        )
        self.compares = compares

    def __str__(
        self,
    ) -> str:

        if isinstance(self.compares, dict):
            return str(
                [compare_set_name for compare_set_name in self.compares.keys()],
            )

        else:
            return str(
                self.compares,
            )

    @log_exception
    def __setitem__(
        self,
        key: str,
        value: Compare,
    ) -> None:
        if self.compares is None:
            self.compares = {}

        if not isinstance(self.compares, dict):
            raise TypeError(
                'CompareSet collection is not a dictionary!',
            )

        self.compares[key] = value

    @log_exception
    def __getitem__(
        self,
        item: str,
    ) -> Compare:

        if self.compares is None:
            raise ValueError(
                'CompareSet object is empty!',
            )

        if not isinstance(self.compares, dict):
            raise TypeError(
                'CompareSet collection is not a dictionary!',
            )

        return self.compares[item]

    @log_exception
    @log_runtime
    def load(
        self,
    ) -> None:

        # TODO: Multiprocess load each compare
        pass

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

        return CompareSet(
            description=instance_data['description'],
            compares={
                name: Compare.deserialize(
                    instance_data=compare_set_values,
                    working_dir_path=working_dir_path,
                    ib2d_file=ib2d_file,
                    data_sources=data_sources,
                    wildcard_sets=wildcard_sets,
                )
                for name, compare_set_values in instance_data['compares'].items()
            },
        )

    @log_exception
    def serialize(
        self,
        ib2d_file: ZipFile,
    ) -> Dict:

        return {
            'description': self.description.value,
            'compares': {
                name: instance.serialize(
                    ib2d_file=ib2d_file,
                )
                for name, instance in self.compares.items()
            },
        }
