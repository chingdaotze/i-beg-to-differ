from .input_field_group_box import InputFieldGroupBox
from .......core.input_fields.wildcard_input_fields import WildcardDictInputField
from .dict_table_widget import WildcardDictTableWidget


class WildcardDictInputFieldGroupBox(
    InputFieldGroupBox,
):

    input_field: WildcardDictInputField
    dict_table: WildcardDictTableWidget

    def __init__(
        self,
        input_field: WildcardDictInputField,
    ) -> None:

        InputFieldGroupBox.__init__(
            self=self,
            input_field=input_field,
        )

        self.dict_table = WildcardDictTableWidget(
            values=input_field.values,
            key_column=input_field.key_column,
            value_column=input_field.value_column,
        )

        self.layout.addWidget(
            self.dict_table,
        )
