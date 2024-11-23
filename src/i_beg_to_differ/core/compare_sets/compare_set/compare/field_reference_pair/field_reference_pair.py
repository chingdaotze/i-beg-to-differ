from abc import ABC

from .....base import Base
from .field_reference import FieldReference
from ..data_source_reference import DataSourceReference
from .....data_sources.data_source.field.field_transforms import FieldTransforms
from .....wildcards_sets import WildcardSets


class FieldReferencePair(
    Base,
    ABC,
):
    """
    Pair of Field References. Functions as a pointer to underlying
    Data Source > Field > Transform data structure.
    """

    source_field_ref: FieldReference
    """
    Source field pointer.
    """

    target_field_ref: FieldReference
    """
    Target field pointer.
    """

    is_primary_key: bool
    """
    Indicator for whether this field pair is a primary key.
    """

    _source_data_source_ref: DataSourceReference
    _target_data_source_ref: DataSourceReference

    def __init__(
        self,
        source_field_name: str,
        source_data_source_ref: DataSourceReference,
        target_field_name: str,
        target_data_source_ref: DataSourceReference,
        source_field_transforms: FieldTransforms | None = None,
        target_field_transforms: FieldTransforms | None = None,
        wildcard_sets: WildcardSets | None = None,
    ):

        Base.__init__(
            self=self,
        )

        self._source_data_source_ref = source_data_source_ref

        self.source_field_ref = FieldReference(
            field_name=source_field_name,
            transforms=source_field_transforms,
            data_source_ref=self.source_data_source_ref,
            wildcard_sets=wildcard_sets,
        )

        self._target_data_source_ref = target_data_source_ref

        self.target_field_ref = FieldReference(
            field_name=target_field_name,
            transforms=target_field_transforms,
            data_source_ref=self.target_data_source_ref,
            wildcard_sets=wildcard_sets,
        )

    def __str__(
        self,
    ) -> str:

        return f'{self.source_field_ref} | {self.target_field_ref}'

    @property
    def source_data_source_ref(
        self,
    ) -> DataSourceReference:
        """
        Source data source pointer.
        """

        return self._source_data_source_ref

    @source_data_source_ref.setter
    def source_data_source_ref(
        self,
        value: DataSourceReference,
    ) -> None:
        """
        Source data source pointer. Synchronizes source data source to field reference.
        """

        self._source_data_source_ref = value
        self.source_field_ref.data_source_ref = self._source_data_source_ref

    @property
    def target_data_source_ref(
        self,
    ) -> DataSourceReference:
        """
        Source data source pointer.
        """

        return self._source_data_source_ref

    @target_data_source_ref.setter
    def target_data_source_ref(
        self,
        value: DataSourceReference,
    ) -> None:
        """
        Target data source pointer. Synchronizes target data source to field reference.
        """

        self._target_data_source_ref = value
        self.target_field_ref.data_source_ref = self._target_data_source_ref
