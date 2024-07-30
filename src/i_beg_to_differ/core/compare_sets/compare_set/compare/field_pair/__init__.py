from pathlib import Path
from typing import (
    List,
    Dict,
    Self,
)
from zipfile import ZipFile

from .....ib2d_file.ib2d_file_element import IB2DFileElement
from .....base import log_exception
from .....data_sources.data_source.field import Field
from .field_pair_compare_rule import FieldPairCompareRule
from .....wildcards_sets import WildcardSets


class FieldPair(
    IB2DFileElement,
):
    """
    Pair of Fields for comparison.
    """

    source: Field
    target: Field

    compare_rules: List[FieldPairCompareRule]

    def __init__(
        self,
        working_dir_path: Path,
        source: Field,
        target: Field,
    ):

        IB2DFileElement.__init__(
            self=self,
            module_name=__name__,
            working_dir_path=working_dir_path,
        )

        self.source = source
        self.target = target

    def __str__(
        self,
    ) -> str:

        return f"{self.source} | {self.target}"

    @classmethod
    @log_exception
    def deserialize(
        cls,
        instance_data: Dict,
        working_dir_path: Path,
        ib2d_file: ZipFile,
        wildcard_sets: WildcardSets | None = None,
    ) -> Self:

        source = Field.deserialize(
            instance_data=instance_data["source"],
            working_dir_path=working_dir_path,
            ib2d_file=ib2d_file,
            wildcard_sets=wildcard_sets,
        )

        target = Field.deserialize(
            instance_data=instance_data["target"],
            working_dir_path=working_dir_path,
            ib2d_file=ib2d_file,
            wildcard_sets=wildcard_sets,
        )

        instance = FieldPair(
            working_dir_path=working_dir_path,
            source=source,
            target=target,
        )

        return instance

    @log_exception
    def serialize(
        self,
        ib2d_file: ZipFile,
    ) -> Dict:

        instance_data = {
            "source": self.source.serialize(
                ib2d_file=ib2d_file,
            ),
            "target": self.target.serialize(
                ib2d_file=ib2d_file,
            ),
            "compare_rules": [
                instance.serialize(
                    ib2d_file=ib2d_file,
                )
                for instance in self.compare_rules
            ],
        }

        return instance_data
