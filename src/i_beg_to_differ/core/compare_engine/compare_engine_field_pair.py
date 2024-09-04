from ..compare_sets.compare_set.compare.field_pair import FieldPair


class CompareEngineFieldPair(
    FieldPair,
):
    """
    Compare engine abstract layer, allowing the compare engine to
    use one set of field names while maintaining linkage to original
    field names.
    """

    _source_field_name: str
    """
    Source field name used in the compare engine.
    """

    _target_field_name: str
    """
    Target field name used in the compare engine.
    """

    def __init__(
        self,
        field_pair: FieldPair,
        source_field_name: str | None = None,
        target_field_name: str | None = None,
    ):

        FieldPair.__init__(
            self=self,
            source_field=field_pair.source_field.base_value,
            source_transforms=field_pair.source_transforms,
            target_field=field_pair.target_field.base_value,
            target_transforms=field_pair.target_transforms,
        )

        if source_field_name is None:
            self._source_field_name = str(
                self.source_field,
            )

        else:
            self._source_field_name = source_field_name

        if target_field_name is None:
            self._target_field_name = str(
                self.target_field,
            )

        else:
            self._target_field_name = target_field_name

    @property
    def source_field_name(
        self,
    ) -> str:
        if self.source_transforms:
            return f'{self._source_field_name}(T*)'

        else:
            return self._source_field_name

    @property
    def target_field_name(
        self,
    ) -> str:
        if self.target_transforms:
            return f'{self._target_field_name}(T*)'

        else:
            return self._target_field_name
