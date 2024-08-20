from .code_editor import CodeEditor
from .. import Extensions


class CodeEditorExtensions[CodeEditor](
    Extensions,
):
    """
    Contains and manages all available code editors for this package.
    """

    def __init__(
        self,
    ):
        Extensions.__init__(
            self=self,
            path=__path__,
            name=__name__,
        )
