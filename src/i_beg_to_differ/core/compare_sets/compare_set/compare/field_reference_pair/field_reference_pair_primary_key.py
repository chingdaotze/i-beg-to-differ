from .field_reference_pair import FieldReferencePair
from ..data_source_reference import DataSourceReference
from .....data_sources.data_source.field.field_transforms import FieldTransforms
from .....wildcards_sets import WildcardSets


class FieldReferencePairPrimaryKey(
    FieldReferencePair,
):
    """
    Pair of primary key references for aligning data fields.
    """

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

        FieldReferencePair.__init__(
            self=self,
            source_field_name=source_field_name,
            source_data_source_ref=source_data_source_ref,
            source_field_transforms=source_field_transforms,
            target_field_name=target_field_name,
            target_data_source_ref=target_data_source_ref,
            target_field_transforms=target_field_transforms,
            wildcard_sets=wildcard_sets,
        )
