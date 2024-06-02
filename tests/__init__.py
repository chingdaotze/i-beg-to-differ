from pathlib import Path
from logging import FileHandler

from i_beg_to_differ.core import setup_logger


log_file_path = Path(__file__).parent / 'test_artifacts' / 'ib2d_test.log'

setup_logger(
    file_handler=FileHandler(
        filename=log_file_path,
        mode='w',
    ),
)
