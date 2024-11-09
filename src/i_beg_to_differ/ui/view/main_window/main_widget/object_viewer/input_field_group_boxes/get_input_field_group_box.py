from typing import Any

from PySide6.QtWidgets import QGroupBox

from .......core.input_fields import (
    InputField,
    DictInputField,
    TextBoxInputField,
)
from .......core.input_fields.wildcard_input_fields import (
    WildcardDictInputField,
    WildcardInputField,
    WildcardPathInputField,
)
from .dict_input_field_group_box import DictInputFieldGroupBox
from .text_box_input_field_group_box import TextBoxInputFieldGroupBox
from .wildcard_dict_input_field_group_box import WildcardDictInputFieldGroupBox
from .wildcard_input_field_group_box import WildcardInputFieldGroupBox
from .wildcard_path_input_field_group_box import WildcardPathInputFieldGroupBox


def get_input_field_group_box(
    member: Any,
) -> QGroupBox | None:
    member_type = type(
        member,
    )

    if issubclass(member_type, InputField):
        if member_type == DictInputField:
            return DictInputFieldGroupBox(
                input_field=member,
            )

        elif member_type == TextBoxInputField:
            return TextBoxInputFieldGroupBox(
                input_field=member,
            )

        elif member_type == WildcardDictInputField:
            return WildcardDictInputFieldGroupBox(
                input_field=member,
            )

        elif member_type == WildcardInputField:
            return WildcardInputFieldGroupBox(
                input_field=member,
            )

        elif member_type == WildcardPathInputField:
            return WildcardPathInputFieldGroupBox(
                input_field=member,
            )

        else:
            raise NotImplementedError(
                f'InputField type not implemented: {type(member)}!'
            )

    else:
        return None
