import logging
from pathlib import Path


def get_logger(name):
    """Custom logging function."""
    log_path = Path('~/.playx/logs/log.cat')

    # if log_path.is_fifo():
    log_path = log_path.expanduser()

    log_format = "[%(name)s]: %(message)s"
    logging.basicConfig(level=logging.INFO,
                        format=log_format,
                        filename=log_path)
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    console.setFormatter(logging.Formatter(log_format))
    logging.getLogger(name).addHandler(console)
    return logging.getLogger(name)
