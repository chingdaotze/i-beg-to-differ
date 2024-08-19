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
from .....data_sources.data_source import DataSource, FieldTransforms
from .....wildcards_sets import WildcardSets


class FieldPair(
    IB2DFileElement,
):
    """
    Pair of Fields for comparison.
    """

    source_field: Field
    """
    Source field object. Contains source data for compare.
    """

    source_transforms: FieldTransforms
    """
    List of transformations applied to the source field.
    """

    target_field: Field
    """
    Target field object. Contains target data for compare.
    """

    target_transforms: FieldTransforms
    """
    List of transformations applied to the target field
    """

    compare_rules: List[FieldPairCompareRule]

    def __init__(
        self,
        working_dir_path: Path,
        source_field: Field,
        source_transforms: FieldTransforms,
        target_field: Field,
        target_transforms: FieldTransforms,
    ):

        IB2DFileElement.__init__(
            self=self,
            module_name=__name__,
            working_dir_path=working_dir_path,
        )

        self.source_field = source_field
        self.source_transforms = source_transforms
        self.target_field = target_field
        self.target_transforms = target_transforms

    def __str__(
        self,
    ) -> str:

        return f'{self.source_field} | {self.target_field}'

    @classmethod
    @log_exception
    def deserialize(
        cls,
        instance_data: Dict,
        working_dir_path: Path,
        ib2d_file: ZipFile,
        source_data_source: DataSource,
        target_data_source: DataSource,
        wildcard_sets: WildcardSets | None = None,
    ) -> Self:

        source_field_name = instance_data['source']['name']
        source_field = source_data_source[source_field_name]
        source_transforms = FieldTransforms.deserialize(
            instance_data=instance_data['source']['transforms'],
            working_dir_path=working_dir_path,
            ib2d_file=ib2d_file,
            wildcard_sets=wildcard_sets,
        )

        target_field_name = instance_data['target']['name']
        target_field = target_data_source[target_field_name]
        target_transforms = FieldTransforms.deserialize(
            instance_data=instance_data['target']['transforms'],
            working_dir_path=working_dir_path,
            ib2d_file=ib2d_file,
            wildcard_sets=wildcard_sets,
        )

        instance = FieldPair(
            working_dir_path=working_dir_path,
            source_field=source_field,
            source_transforms=source_transforms,
            target_field=target_field,
            target_transforms=target_transforms,
        )

        return instance

    @log_exception
    def serialize(
        self,
        ib2d_file: ZipFile,
    ) -> Dict:

        instance_data = {
            'source': self.source_field.serialize(
                ib2d_file=ib2d_file,
            ),
            'target': self.target_field.serialize(
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
