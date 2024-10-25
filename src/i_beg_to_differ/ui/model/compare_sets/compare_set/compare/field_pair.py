from ....base import ModelBase
from ......core.compare_sets.compare_set.compare.field_pair import FieldPair


class ModelFieldPair(
    ModelBase,
):

    def __init__(
        self,
        field_pair: FieldPair,
    ):

        ModelBase.__init__(
            self=self,
            current_state=field_pair,
        )
