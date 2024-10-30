from typing import Any

from PySide6.QtWidgets import QLayout

from .......core.extensions.input_fields import (
    InputField,
    StringInputField,
)
from .string_input_field import ObjectViewerStringInputField


def get_object_viewer_layout(
    member: Any,
) -> QLayout | None:
    if issubclass(type(member), InputField):
        if isinstance(member, StringInputField):
            return ObjectViewerStringInputField(
                input_field=member,
            )

        else:
            raise NotImplementedError(
                f'InputField type not implemented: {type(member)}!'
            )

    else:
        return None
