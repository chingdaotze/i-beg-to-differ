from abc import ABC

from .....base import Base
from .....input_fields.wildcard_input_fields import WildcardInputField
from .....data_sources.data_source.field.field_transforms import FieldTransforms
from .....wildcards_sets import WildcardSets


class FieldPair(
    Base,
    ABC,
):
    """
    Pair of Fields. Functions as a pointer to underlying
    Data Source > Field > Transform data structure.
    """

    source_field: WildcardInputField
    """
    Source field name. Used as a pointer to the source field.
    """

    source_transforms: FieldTransforms
    """
    List of transformations applied to the source field.
    """

    target_field: WildcardInputField
    """
    Source field name. Used as a pointer to the target field.
    """

    target_transforms: FieldTransforms
    """
    List of transformations applied to the target field.
    """

    def __init__(
        self,
        source_field: str,
        target_field: str,
        source_transforms: FieldTransforms | None = None,
        target_transforms: FieldTransforms | None = None,
        wildcard_sets: WildcardSets | None = None,
    ):

        Base.__init__(
            self=self,
        )

        self.source_field = WildcardInputField(
            base_value=source_field,
            title='Source',
            wildcard_sets=wildcard_sets,
        )

        self.target_field = WildcardInputField(
            base_value=target_field,
            title='Target',
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

    @property
    def source_field_name(
        self,
    ) -> str:
        """
        Unique identifier for the source field.

        :return:
        """

        source_field_name = f'src.[{self.source_field}]'

        if self.source_transforms:
            source_field_name = f'{source_field_name} >> {self.source_transforms}'

        return source_field_name

    @property
    def source_field_name_short(
        self,
    ) -> str:
        """
        Truncated identifier for the source field, used in reports.

        :return:
        """

        source_field_name = f'src.[{self.source_field}]'

        if self.source_transforms:
            source_field_name = f'{source_field_name}(T*)'

        return source_field_name

    @property
    def target_field_name(
        self,
    ) -> str:
        """
        Unique identifier for the target field.

        :return:
        """

        target_field_name = f'tgt.[{self.target_field}]'

        if self.target_transforms:
            target_field_name = f'{target_field_name} >> {self.target_transforms}'

        return target_field_name

    @property
    def target_field_name_short(
        self,
    ) -> str:
        """
        Truncated identifier for the target field, used in reports.

        :return:
        """

        target_field_name = f'tgt.[{self.target_field}]'

        if self.target_transforms:
            target_field_name = f'{target_field_name}(T*)'

        return target_field_name
