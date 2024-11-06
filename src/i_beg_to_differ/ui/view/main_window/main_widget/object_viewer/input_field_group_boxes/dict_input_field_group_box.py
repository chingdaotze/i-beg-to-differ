from .input_field_group_box import InputFieldGroupBox
from .......core.input_fields import DictInputField
from .dict_table_widget import DictTableWidget


class DictInputFieldGroupBox(
    InputFieldGroupBox,
):

    input_field: DictInputField
    dict_table: DictTableWidget

    def __init__(
        self,
        input_field: DictInputField,
    ) -> None:

        InputFieldGroupBox.__init__(
            self=self,
            input_field=input_field,
        )

        self.dict_table = DictTableWidget(
            values=input_field.values,
            key_column=input_field.key_column,
            value_column=input_field.value_column,
        )

        self.layout.addWidget(
            self.dict_table,
        )
