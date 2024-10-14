from pathlib import Path

from .fixture_ib2d_file import ib2d_file
from i_beg_to_differ.core import IB2DFile


def test_python_edit(
    ib2d_file: IB2DFile,
    tmp_path: Path,
) -> None:
    with ib2d_file:

        compare_set = ib2d_file.compare_sets['CompareSet0']
        compare = compare_set['Compare1']

        compare.dt_fields[0].source_transforms.transforms[0].edit_python_file()

        report_path = tmp_path / 'report.xlsx'
        compare.to_excel(
            path=report_path,
        )
