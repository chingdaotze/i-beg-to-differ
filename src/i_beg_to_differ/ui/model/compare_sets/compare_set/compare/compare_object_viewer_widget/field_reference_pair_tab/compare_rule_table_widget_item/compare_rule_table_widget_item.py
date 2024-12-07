from pathlib import Path

from .........core.compare_sets.compare_set.compare.field_reference_pair import (
    FieldReferencePairData,
)
from ........widgets import TableWidgetItemDialog
from .compare_rule_table_widget_item_dialog import CompareRuleTableWidgetItemDialog


class CompareRuleTableWidgetItem(
    TableWidgetItemDialog,
):

    field_reference_pair: FieldReferencePairData
    working_dir_path: Path

    def __init__(
        self,
        field_reference_pair: FieldReferencePairData,
        working_dir_path: Path,
    ):

        self.field_reference_pair = field_reference_pair
        self.working_dir_path = working_dir_path

        TableWidgetItemDialog.__init__(
            self=self,
        )

    def get_text(
        self,
    ) -> str:

        return str(
            self.field_reference_pair.compare_rule,
        )

    def open_dialog(
        self,
    ) -> None:

        dialog = CompareRuleTableWidgetItemDialog(
            field_reference_pair=self.field_reference_pair,
            working_dir_path=self.working_dir_path,
        )

        dialog.exec()
