from logging import (
    getLogger,
    DEBUG,
    Formatter,
    FileHandler,
    StreamHandler,
)

from .ib2d_file import IB2DFile


def setup_logger(
    file_handler: FileHandler | None = None,
    stream_handler: StreamHandler | None = None,
    level: int = DEBUG,
) -> None:
    """
    Sets up the logging module.

    :param file_handler: File handler for the logger. If not provided, does not log to a file.
    :param stream_handler: Stream handler for the logger. If not provided, uses a default StreamHandler.
    :param level: Minimum logging level.
    :return:
    """

    # Create logger
    logger = getLogger(
        __name__,
    )

    logger.setLevel(
        level=level,
    )

    # Create formatter
    fmt = Formatter(
        fmt='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
    )

    # Add stream handler
    if stream_handler is None:
        stream_handler = StreamHandler()

    stream_handler.setLevel(
        level=logger.level,
    )
    stream_handler.setFormatter(
        fmt=fmt,
    )

    logger.addHandler(
        hdlr=stream_handler,
    )

    # Add file handler
    if isinstance(file_handler, FileHandler):
        file_handler.setLevel(
            level=logger.level,
        )
        file_handler.setFormatter(
            fmt=fmt,
        )

        logger.addHandler(
            hdlr=file_handler,
        )


open_ib2d_file = IB2DFile.open
