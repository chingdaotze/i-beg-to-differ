from pathlib import Path

from .fixture_ib2d_file import ib2d_file

from i_beg_to_differ.core import IB2DFile


def test_serialize_ib2d_file(
    ib2d_file: IB2DFile,
    tmpdir: Path,
) -> None:
    # Get benchmark hash
    ib2d_zip_file = ib2d_file.load_zip_file(
        path=ib2d_file.path,
    )

    benchmark_file_crc = {
        deflated_file.filename: deflated_file.CRC
        for deflated_file in ib2d_zip_file.filelist
    }

    # Serialize
    module_name = __name__.split('.')[-1]

    ib2d_save_path = Path(
        tmpdir / f'{module_name}.ib2d',
    )

    ib2d_file.save(
        path=ib2d_save_path,
    )

    # Get new file hash
    ib2d_zip_file = ib2d_file.load_zip_file(
        path=ib2d_save_path,
    )

    new_file_crc = {
        deflated_file.filename: deflated_file.CRC
        for deflated_file in ib2d_zip_file.filelist
    }

    assert benchmark_file_crc == new_file_crc
