from pathlib import Path
from typing import (
    List,
    Dict,
    Self,
)
from zipfile import ZipFile

from ..ib2d_file.ib2d_file_element import IB2DFileElement
from .compare import Compare
from ..wildcards import Wildcards


class CompareSet(
    IB2DFileElement,
):
    """
    Compare set object. Contains a collection of compares.
    """

    compares: List[Compare]

    def __init__(
        self,
        working_dir_path: Path,
        wildcards: Wildcards | None = None,
        compares: List | None = None,
    ):
        IB2DFileElement.__init__(
            self=self,
            working_dir_path=working_dir_path,
            wildcards=wildcards,
        )

        self.compares = compares

    @IB2DFileElement.wildcards.setter
    def wildcards(
        self,
        wildcards: Wildcards,
    ) -> None:

        self._wildcards = wildcards

        for instance in self.compares:
            instance.wildcards = wildcards

    @classmethod
    def deserialize(
        cls,
        instance_data: Dict,
        working_dir_path: Path,
        ib2d_file: ZipFile,
    ) -> Self:
        # Construct object
        compares = [
            Compare.deserialize(
                instance_data=compare_instance_data,
                working_dir_path=working_dir_path,
                ib2d_file=ib2d_file,
            )
            for compare_instance_data in instance_data['compare_set']
        ]

        instance = CompareSet(
            working_dir_path=working_dir_path,
            compares=compares,
        )

        # Set wildcards
        wildcards = Wildcards.deserialize(
            instance_data=instance_data['wildcards'],
            working_dir_path=working_dir_path,
            ib2d_file=ib2d_file,
        )

        instance.wildcards = wildcards

        return instance

    def serialize(
        self,
        ib2d_file: ZipFile,
    ) -> Dict:

        instance_data = {
            'compares': [
                instance.serialize(
                    ib2d_file=ib2d_file,
                )
                for instance in self.compares
            ],
            'wildcards': self.wildcards.serialize(
                ib2d_file=ib2d_file,
            ),
        }

        return instance_data
