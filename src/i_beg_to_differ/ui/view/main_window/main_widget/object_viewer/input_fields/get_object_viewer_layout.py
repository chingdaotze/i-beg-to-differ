from typing import (
    Any,
    List,
)

from PySide6.QtWidgets import (
    QLayout,
    QLayoutItem,
    QWidget,
)

from .......core.extensions.input_fields import (
    InputField,
    DictInputField,
    ListInputField,
    PathInputField,
    StringInputField,
    WildcardInputField,
)
from .path_input_field import ObjectViewerPathInputField
from .string_input_field import ObjectViewerStringInputField
from .wildcard_input_field import ObjectViewerWildcardInputField


def get_object_viewer_layout(
    member: Any,
) -> QLayout | List[List[QLayoutItem]] | None:
    if issubclass(type(member), InputField):
        if isinstance(member, DictInputField):
            pass

        elif isinstance(member, ListInputField):
            pass

        elif isinstance(member, PathInputField):
            return ObjectViewerPathInputField(
                input_field=member,
            )

        elif isinstance(member, StringInputField):
            return ObjectViewerStringInputField(
                input_field=member,
            )

        elif isinstance(member, WildcardInputField):
            return ObjectViewerWildcardInputField(
                input_field=member,
            )

        else:
            raise NotImplementedError(
                f'InputField type not implemented: {type(member)}!'
            )

    else:
        return None
