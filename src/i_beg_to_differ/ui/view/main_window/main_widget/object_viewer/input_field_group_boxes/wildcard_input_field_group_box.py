from .wildcard_input_field_group_box_base import WildcardInputFieldGroupBoxBase
from .wildcard_input_field_widget import WildcardInputFieldWidget
from .......core.input_fields.wildcard_input_fields import WildcardInputField


class WildcardInputFieldGroupBox(
    WildcardInputFieldGroupBoxBase,
):

    input_field: WildcardInputField
    input_widget: WildcardInputFieldWidget

    def __init__(
        self,
        input_field: WildcardInputField,
    ):

        WildcardInputFieldGroupBoxBase.__init__(
            self=self,
            input_field=input_field,
        )

        self.input_widget = WildcardInputFieldWidget(
            input_field=input_field,
            text_changed_callback=self.update_preview,
            parent=self,
        )

        self.layout.addWidget(
            self.input_widget,
            0,
            0,
        )

        self.layout.addWidget(
            self.preview,
            1,
            0,
        )
