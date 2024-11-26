from ....base import Base
from ....wildcards_sets.wildcard_field import WildcardField
from ....wildcards_sets import WildcardSets


class DataSourceReference(
    Base,
):
    """
    Pointer to a Data Source.
    """

    data_source_name: WildcardField
    """
    Name of the data source.
    """

    def __init__(
        self,
        data_source_name: str,
        wildcard_sets: WildcardSets | None = None,
    ):

        Base.__init__(
            self=self,
        )

        self.data_source_name = WildcardField(
            base_value=data_source_name,
            wildcard_sets=wildcard_sets,
        )

    def __str__(
        self,
    ):

        return str(
            self.data_source_name,
        )
