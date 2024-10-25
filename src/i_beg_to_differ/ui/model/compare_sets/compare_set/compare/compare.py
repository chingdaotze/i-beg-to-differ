from ....base import ModelBase
from ......core.compare_sets.compare_set.compare import Compare
from .field_pair import ModelFieldPair


class ModelCompare(
    ModelBase,
):

    def __init__(
        self,
        object_name: str,
        compare: Compare,
    ):

        ModelBase.__init__(
            self=self,
            current_state=compare,
            object_name=object_name,
        )

        for field_pair in compare.fields:

            self.appendRow(
                ModelFieldPair(
                    field_pair=field_pair,
                )
            )
