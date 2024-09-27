from pathlib import Path
from typing import (
    Dict,
    Self,
)
from zipfile import ZipFile

from .field_pair import FieldPair
from .....ib2d_file.ib2d_file_element import IB2DFileElement
from .....base import log_exception
from .....data_sources.data_source.field.field_transforms import FieldTransforms
from .....wildcards_sets import WildcardSets
from .....wildcards_sets.wildcard_field import WildcardField


class FieldPairPrimaryKey(
    FieldPair,
    IB2DFileElement,
):
    """
    Pair of primary keys for aligning data fields.
    """

    def __init__(
        self,
        source_field: str | WildcardField,
        target_field: str | WildcardField,
        source_transforms: FieldTransforms | None = None,
        target_transforms: FieldTransforms | None = None,
        wildcard_sets: WildcardSets | None = None,
    ):

        FieldPair.__init__(
            self=self,
            source_field=source_field,
            target_field=target_field,
            source_transforms=source_transforms,
            target_transforms=target_transforms,
            wildcard_sets=wildcard_sets,
        )

        IB2DFileElement.__init__(
            self=self,
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

        instance = FieldPairPrimaryKey(
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
                'name': self.source_field.base_value,
            }
            | self.source_transforms.serialize(
                ib2d_file=ib2d_file,
            ),
            'target': {
                'name': self.target_field.base_value,
            }
            | self.target_transforms.serialize(
                ib2d_file=ib2d_file,
            ),
        }

        return instance_data
