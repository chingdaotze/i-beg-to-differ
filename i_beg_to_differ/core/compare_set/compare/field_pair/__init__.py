from pathlib import Path
from typing import (
    List,
    Dict,
    Self,
)
from zipfile import ZipFile

from ....ib2d_file.ib2d_file_element import IB2DFileElement
from .field import Field
from ....compare_rules.compare_rule import CompareRule
from ....wildcards import Wildcards


class FieldPair(
    IB2DFileElement,
):
    """
    Pair of Fields for comparison.
    """

    source: Field
    target: Field

    compare_rules: List[CompareRule]

    def __init__(
        self,
        working_dir_path: Path,
        source: Field,
        target: Field,
        wildcards: Wildcards | None = None,
    ):

        IB2DFileElement.__init__(
            self=self,
            working_dir_path=working_dir_path,
            wildcards=wildcards,
        )

        self.source = source
        self.target = target

    @classmethod
    def deserialize(
        cls,
        instance_data: Dict,
        working_dir_path: Path,
        ib2d_file: ZipFile,
        wildcards: Wildcards | None = None,
    ) -> Self:

        source = Field.deserialize(
            instance_data=instance_data['source'],
            working_dir_path=working_dir_path,
            ib2d_file=ib2d_file,
            wildcards=wildcards,
        )

        target = Field.deserialize(
            instance_data=instance_data['target'],
            working_dir_path=working_dir_path,
            ib2d_file=ib2d_file,
            wildcards=wildcards,
        )

        instance = FieldPair(
            working_dir_path=working_dir_path,
            source=source,
            target=target,
            wildcards=wildcards,
        )

        return instance

    def serialize(
        self,
        ib2d_file: ZipFile,
    ) -> Dict:

        instance_data = {
            'source': self.source.serialize(
                ib2d_file=ib2d_file,
            ),
            'target': self.target.serialize(
                ib2d_file=ib2d_file,
            ),
            'compare_rules': [
                instance.serialize(
                    ib2d_file=ib2d_file,
                )
                for instance in self.compare_rules
            ],
        }

        return instance_data
