from enum import StrEnum
from typing_extensions import Annotated
from pathlib import Path
from logging import FileHandler

from typer import (
    Typer,
    Argument,
    Option,
)
from PySide6.QtWidgets import QApplication

from i_beg_to_differ.core import (
    open_ib2d_file,
    setup_logger,
)
from i_beg_to_differ.ui import MainWindow


typer_app = Typer()


class OutputFormat(
    StrEnum,
):
    CSV = 'csv'
    XLSX = 'xlsx'
    PARQUET = 'parquet'


@typer_app.command()
def cli(
    ib2d_file_path: Annotated[
        str,
        Argument(
            help='Path to an *.ib2d file.',
        ),
    ],
    compare_set: Annotated[
        str,
        Argument(
            help='Compare set to run.',
        ),
    ],
    compare: Annotated[
        str,
        Argument(
            help='Compare to run.',
        ),
    ],
    output_path: Annotated[
        str,
        Argument(
            help='Path to the report output.',
        ),
    ],
    output_format: Annotated[
        OutputFormat,
        Option(
            help='Report output format.',
        ),
    ] = OutputFormat.CSV,
    active_wildcard_set: Annotated[
        str,
        Option(
            help='Active wildcard set to use. Defaults to the default wildcard set.',
        ),
    ] = None,
) -> None:
    """
    Command-line interface for the i-beg-to-differ package.
    Generates a comparison report given an *.ib2d file path.
    """

    with open_ib2d_file(path=ib2d_file_path) as ib2d_file:

        if active_wildcard_set is not None:
            ib2d_file.wildcard_sets.active_wildcard_set = active_wildcard_set

        compare_set = ib2d_file[compare_set]
        compare = compare_set[compare]

        match output_format:
            case OutputFormat.CSV:
                compare.to_csv(
                    dir_path=output_path,
                )

            case OutputFormat.XLSX:
                compare.to_excel(
                    path=output_path,
                )

            case OutputFormat.PARQUET:
                compare.to_excel(
                    path=output_path,
                )

            case _:

                raise NotImplementedError(
                    f'Unhandled output format: {output_format}',
                )


@typer_app.command()
def gui(
    ib2d_file_path: Annotated[
        str,
        Option(
            help='Path to an *.ib2d file. Loads the *.ib2d file into the GUI.',
        ),
    ] = None,
) -> None:

    qt_app = QApplication()

    main_window = MainWindow()
    main_window.show()

    qt_app.exec()


if __name__ == '__main__':
    run_dir = Path(
        __file__,
    ).parent

    log_file_path = run_dir / 'i_beg_to_differ.log'

    setup_logger(
        file_handler=FileHandler(
            filename=log_file_path,
            mode='w',
        ),
    )

    typer_app()
