from ....base import Base
from ....input_fields.wildcard_input_fields import WildcardInputField
from ....wildcards_sets import WildcardSets


class DataSourceReference(
    Base,
):
    """
    Pointer to a Data Source.
    """

    data_source_name: WildcardInputField
    """
    Name of the data source.
    """

    def __init__(
        self,
        data_source_name: str,
        title: str | None = None,
        wildcard_sets: WildcardSets | None = None,
    ):

        Base.__init__(
            self=self,
        )

        self.data_source_name = WildcardInputField(
            base_value=data_source_name,
            title=title,
            wildcard_sets=wildcard_sets,
        )

    def __str__(
        self,
    ):

        return str(
            self.data_source_name,
        )
