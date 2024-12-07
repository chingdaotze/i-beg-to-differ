from pathlib import Path
from typing import (
    List,
    Tuple,
    Type,
)

from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QComboBox,
    QPushButton,
)

from ........widgets import Dialog
from .........core.compare_sets.compare_set.compare.field_reference_pair import (
    FieldReferencePairData,
)
from .........core.compare_sets.compare_set.compare.field_reference_pair.compare_rule import (
    CompareRule,
)
from .........core.extensions.extension.custom_python_extension import (
    CustomPythonExtension,
)


class CompareRuleTableWidgetItemDialog(
    Dialog,
):

    field_reference_pair: FieldReferencePairData
    compare_rule_display: QLabel
    working_dir_path: Path
    extension_name_map: List[Tuple[str, Type[CompareRule]]]

    def __init__(
        self,
        field_reference_pair: FieldReferencePairData,
        working_dir_path: Path,
        parent: QWidget | None = None,
    ):

        Dialog.__init__(
            self,
            title='Compare Rule',
            parent=parent,
        )

        self.field_reference_pair = field_reference_pair
        self.working_dir_path = working_dir_path

        self.extension_name_map = [
            (compare_rule.extension_name, compare_rule)
            for compare_rule in self.field_reference_pair.compare_rule_extensions.collection.values()
        ]

        # Build compare rule display
        self.compare_rule_display = QLabel()

        self.layout.addWidget(
            self.compare_rule_display,
            0,
            0,
        )

        self.update_compare_rule_display()

        # Build edit button
        edit_button = QPushButton(
            'Edit Compare Rule Parameters',
        )

        edit_button.clicked.connect(
            self.click_edit_button,
        )

        self.layout.addWidget(
            edit_button,
            1,
            0,
        )

        # Build change button
        change_button = QPushButton(
            'Change Compare Rule',
        )

        change_button.clicked.connect(
            self.click_change_button,
        )

        self.layout.addWidget(
            change_button,
            2,
            0,
        )

    def update_compare_rule_display(
        self,
    ) -> None:

        self.compare_rule_display.setText(
            str(
                self.field_reference_pair.compare_rule,
            )
        )

    def click_change_button(
        self,
    ) -> None:

        # Build /show selector
        compare_rule_selector_widget = QComboBox(
            self,
        )

        compare_rule_selector_widget.addItems(
            [
                extension_name_mapping[0]
                for extension_name_mapping in self.extension_name_map
            ],
        )

        dialog = Dialog(
            title='Change Compare Rule',
        )

        dialog.layout.addWidget(
            compare_rule_selector_widget,
            0,
            0,
        )

        dialog.exec()

        # Retrieve / set compare new rule
        current_index = compare_rule_selector_widget.currentIndex()
        compare_rule_type = self.extension_name_map[current_index][1]

        if issubclass(compare_rule_type, CustomPythonExtension):
            compare_rule = compare_rule_type(
                working_dir_path=self.working_dir_path,
            )

        else:
            compare_rule = compare_rule_type()

        self.field_reference_pair.compare_rule = compare_rule
        self.update_compare_rule_display()

    def click_edit_button(
        self,
    ) -> None:

        dialog = Dialog(
            title='Compare Rule Parameters',
        )

        dialog.layout.addWidget(
            self.field_reference_pair.compare_rule.object_viewer_widget,
            0,
            0,
        )

        dialog.exec()

        self.update_compare_rule_display()
