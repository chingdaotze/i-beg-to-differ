from pathlib import Path
from typing import (
    List,
    Dict,
    Self,
)
from zipfile import ZipFile

from .....ib2d_file.ib2d_file_element import IB2DFileElement
from .....wildcards_sets.wildcard_field import WildcardField
from .....base import log_exception
from .....data_sources.data_source.field.field_transforms import FieldTransforms
from .field_pair_compare_rule import FieldPairCompareRule
from .....wildcards_sets import WildcardSets


class FieldPair(
    IB2DFileElement,
):
    """
    Pair of Fields for comparison. Functions as a pointer to underlying
    Data Source > Field > Transform data structure.
    """

    source_field: WildcardField
    """
    Source field name. Used as a pointer to the source field.
    """

    source_transforms: FieldTransforms
    """
    List of transformations applied to the source field.
    """

    target_field: WildcardField
    """
    Source field name. Used as a pointer to the target field.
    """

    target_transforms: FieldTransforms
    """
    List of transformations applied to the target field
    """

    compare_rules: List[FieldPairCompareRule]

    def __init__(
        self,
        source_field: str,
        target_field: str,
        source_transforms: FieldTransforms | None = None,
        target_transforms: FieldTransforms | None = None,
        wildcard_sets: WildcardSets | None = None,
    ):

        IB2DFileElement.__init__(
            self=self,
        )

        self.source_field = WildcardField(
            base_value=source_field,
            wildcard_sets=wildcard_sets,
        )

        self.target_field = WildcardField(
            base_value=target_field,
            wildcard_sets=wildcard_sets,
        )

        if source_transforms is None:
            self.source_transforms = FieldTransforms()

        else:
            self.source_transforms = source_transforms

        if target_transforms is None:
            self.target_transforms = FieldTransforms()

        else:
            self.target_transforms = target_transforms

    def __str__(
        self,
    ) -> str:

        return f'{self.source_field_name} | {self.target_field_name}'

    @classmethod
    @log_exception
    def deserialize(
        cls,
        instance_data: Dict,
        working_dir_path: Path,
        ib2d_file: ZipFile,
        wildcard_sets: WildcardSets | None = None,
    ) -> Self:

        source_field = instance_data['source']['name']
        source_transforms = FieldTransforms.deserialize(
            instance_data=instance_data['source']['transforms'],
            working_dir_path=working_dir_path,
            ib2d_file=ib2d_file,
            wildcard_sets=wildcard_sets,
        )

        target_field = instance_data['target']['name']
        target_transforms = FieldTransforms.deserialize(
            instance_data=instance_data['target']['transforms'],
            working_dir_path=working_dir_path,
            ib2d_file=ib2d_file,
            wildcard_sets=wildcard_sets,
        )

        instance = FieldPair(
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
            'source': {
                'name': self.source_field,
            }
            | self.source_transforms.serialize(),
            'target': {
                'name': self.target_field,
            }
            | self.target_transforms.serialize(),
            'compare_rules': [
                instance.serialize(
                    ib2d_file=ib2d_file,
                )
                for instance in self.compare_rules
            ],
        }

        return instance_data

    @property
    def source_field_name(
        self,
    ) -> str:
        """
        Unique identifier for the source field.

        :return:
        """

        source_field_name = f'[{str(self.source_field)}]'

        if self.source_transforms:
            source_field_name = f'{source_field_name} >> {str(self.source_transforms)}'

        return source_field_name

    @property
    def target_field_name(
        self,
    ) -> str:
        """
        Unique identifier for the target field.

        :return:
        """

        target_field_name = f'[{str(self.target_field)}]'

        if self.target_transforms:
            target_field_name = f'{target_field_name} >> {str(self.target_transforms)}'

        return target_field_name
