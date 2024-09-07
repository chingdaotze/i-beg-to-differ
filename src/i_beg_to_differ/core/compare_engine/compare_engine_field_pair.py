from typing import ClassVar

from ..compare_sets.compare_set.compare.field_pair import FieldPair


class CompareEngineFieldPair(
    FieldPair,
):
    """
    Compare engine abstract layer, allowing the compare engine to
    use one set of field names while maintaining linkage to original
    field names.
    """

    source_field_index: int
    """
    Source field index, used to guarantee a unique source field name within a compare.
    """

    target_field_index: int
    """
    Target field index, used to guarantee a unique source field name within a compare.
    """

    _SOURCE_PREFIX: ClassVar[str] = 'src'
    """
    Prefix to assign to source fields.
    """

    _TARGET_PREFIX: ClassVar[str] = 'tgt'
    """
    Prefix to assign to target fields.
    """

    _DIFF_PREFIX: ClassVar[str] = 'dif'
    """
    Prefix to assign to diff fields.
    """

    def __init__(
        self,
        field_pair: FieldPair,
        source_field_index: int,
        target_field_index: int,
    ):

        FieldPair.__init__(
            self=self,
            source_field=field_pair.source_field.base_value,
            source_transforms=field_pair.source_transforms,
            target_field=field_pair.target_field.base_value,
            target_transforms=field_pair.target_transforms,
        )

        self.source_field_index = source_field_index
        self.target_field_index = target_field_index

    @property
    def source_field_name(
        self,
    ) -> str:
        source_field_name = f'{self._SOURCE_PREFIX}.[{str(self.source_field)}]'

        if self.source_transforms:
            source_field_name = f'{source_field_name}(T*)'

        if self.source_field_index > 1:
            source_field_name = f'{source_field_name}({self.source_field_index})'

        return source_field_name

    @property
    def target_field_name(
        self,
    ) -> str:
        target_field_name = f'{self._TARGET_PREFIX}.[{str(self.target_field)}]'

        if self.target_transforms:
            target_field_name = f'{target_field_name}(T*)'

        if self.target_field_index > 1:
            target_field_name = f'{target_field_name}({self.target_field_index})'

        return target_field_name

    @property
    def diff_field_name(
        self,
    ) -> str:
        """
        Unique identifier for the diff field.

        :return:
        """

        return f'{self._DIFF_PREFIX}.{{{str(self)}}}'
