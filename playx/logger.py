import logging
from pathlib import Path


def get_logger(name):
    """Custom logging function."""
    log_path = Path('~/.playx/logs/log.cat')

    log_path = log_path.expanduser()

    log_format = "[{}]: %(message)s".format(name)
    log_format_file = "[{}]-[%(asctime)s]: %(message)s".format(name.upper())
    logging.basicConfig(level=logging.INFO,
                        format=log_format_file,
                        filename=log_path)
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    console.setFormatter(logging.Formatter(log_format, "%Y-%m-%d %H:%M:%S"))
    logging.getLogger(name).addHandler(console)
    return logging.getLogger(name)
