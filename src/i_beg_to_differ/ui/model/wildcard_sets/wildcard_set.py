from ..base import ModelBase
from ....core.wildcards_sets.wildcard_set import WildcardSet


class ModelWildcardSet(
    ModelBase,
):

    _object_name: str

    def __init__(
        self,
        object_name: str,
        wildcard_set: WildcardSet,
    ):
        self._object_name = object_name

        ModelBase.__init__(
            self=self,
            current_state=wildcard_set,
        )

    @property
    def object_name(
        self,
    ) -> str:

        return self._object_name
