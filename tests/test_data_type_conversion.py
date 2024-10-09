from pathlib import Path

from pytest import raises

from .fixture_ib2d_file import ib2d_file
from i_beg_to_differ.core import IB2DFile


def test_data_type_conversion(
    ib2d_file: IB2DFile,
    tmp_path: Path,
) -> None:
    with ib2d_file:

        compare_set = ib2d_file.compare_sets['CompareSet0']
        compare = compare_set['Compare1']

        report_path = tmp_path / 'report.xlsx'

        with raises(
            expected_exception=ValueError,
            match='Unable to parse string "queen" at position 0',
        ):
            compare.to_excel(
                path=report_path,
            )
