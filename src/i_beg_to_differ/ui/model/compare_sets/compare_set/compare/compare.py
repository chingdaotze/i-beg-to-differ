from PySide6.QtWidgets import QScrollArea, QWidget

from ....base import ModelBase
from ......core.compare_sets.compare_set.compare import Compare
from .compare_widget import CompareWidget
from .field_pair import ModelFieldPair


class ModelCompare(
    ModelBase,
):

    current_state: Compare

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

    @property
    def object_viewer_widget(
        self,
    ) -> QWidget | None:

        return CompareWidget(
            compare=self.current_state,
        )
