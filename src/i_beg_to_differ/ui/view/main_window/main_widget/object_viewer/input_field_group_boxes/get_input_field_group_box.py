from typing import Any

from PySide6.QtWidgets import QGroupBox

from .......core.extensions.input_fields import (
    InputField,
    StringInputField,
    WildcardDictInputField,
    WildcardInputField,
    WildcardListInputField,
    WildcardPathInputField,
)
from .string_input_field_group_box import StringInputFieldGroupBox
from .wildcard_input_field_group_box import WildcardInputFieldGroupBox
from .wildcard_path_input_field_group_box import WildcardPathInputGroupBox


def get_input_field_group_box(
    member: Any,
) -> QGroupBox | None:
    member_type = type(
        member,
    )

    if issubclass(member_type, InputField):
        if member_type == StringInputField:
            return StringInputFieldGroupBox(
                input_field=member,
            )

        if member_type == WildcardDictInputField:
            pass

        elif member_type == WildcardInputField:
            return WildcardInputFieldGroupBox(
                input_field=member,
            )

        elif member_type == WildcardListInputField:
            pass

        elif member_type == WildcardPathInputField:
            return WildcardPathInputGroupBox(
                input_field=member,
            )

        else:
            raise NotImplementedError(
                f'InputField type not implemented: {type(member)}!'
            )

    else:
        return None
