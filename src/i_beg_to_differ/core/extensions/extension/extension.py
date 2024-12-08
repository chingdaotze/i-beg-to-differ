from abc import ABC
from typing import ClassVar

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QScrollArea,
    QLabel,
    QTabWidget,
)
from PySide6.QtCore import Qt

from ...base import Base
from ..ui import (
    InputField,
    DescriptionInputField,
)


class Extension(
    Base,
    ABC,
):
    """
    Base class for an IB2D extension.
    """

    extension_name: ClassVar[str]
    """
    Human-readable name for this extension.
    """

    def __init__(
        self,
    ):
        Base.__init__(
            self=self,
        )

    def __str__(
        self,
    ) -> str:

        return self.get_extension_id()

    @classmethod
    def get_extension_id(
        cls,
    ) -> str:
        """
        Gets a unique identifier for this extension, based on the module name.

        :return:
        """

        # FIXME: This is actually a class property, but Python 3.13+ deprecates class properties.

        return cls.__module__.split('.')[-1]

    @property
    def object_viewer_widget(
        self,
    ) -> QWidget:
        """
        Defines this Extension's Object Viewer widget. Override this method to provide a custom widget in the UI.
        By default, this method parses the Extension object for attributes to add to the widget.

        :return: Object Viewer widget.
        """

        # Initialize widget
        input_field_widget = QWidget()
        input_field_layout = QVBoxLayout()

        input_field_widget.setLayout(
            input_field_layout,
        )

        input_field_layout.setAlignment(
            Qt.AlignmentFlag.AlignTop,
        )

        input_field_scroll_area = QScrollArea()

        input_field_scroll_area.setWidget(
            input_field_widget,
        )

        input_field_scroll_area.setWidgetResizable(
            True,
        )

        # Scan for Input Fields
        description_widget = None

        for attribute, value in self.__dict__.items():
            if isinstance(value, DescriptionInputField):
                description_widget = value.layout_component

            elif isinstance(value, InputField):
                input_field_layout.addWidget(
                    value.layout_component,
                )

        # Set default input field widget
        if not input_field_layout.count():
            input_field_layout.addWidget(
                QLabel(
                    'No Object Viewer widget defined for this extension.',
                )
            )

        # Create Description tab
        if description_widget is not None:
            object_viewer_widget = QTabWidget()

            object_viewer_widget.addTab(
                description_widget,
                'Description',
            )

            object_viewer_widget.addTab(
                input_field_scroll_area,
                'Parameters',
            )

        else:
            object_viewer_widget = input_field_scroll_area

        return object_viewer_widget
