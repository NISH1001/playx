import logging
from pathlib import Path


def Logger(name):
    logger = logging.getLogger(name)

    log_path = Path('~/.playx/logs/log.cat').expanduser()

    log_format = "[{}]: %(message)s".format(name)
    log_format_file = "[{}]-[%(asctime)s]: %(message)s".format(name.upper())

    if not len(logging.getLogger().handlers):
        logging.basicConfig(level=logging.INFO,
                            filename=log_path,
                            format=log_format_file
                            )
    else:
        filehandler = logging.FileHandler(log_path)
        filehandler.setLevel(logging.INFO)
        filehandler.setFormatter(logging.Formatter(log_format_file))
        logger.addHandler(filehandler)

    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    console.setFormatter(logging.Formatter(log_format))
    logger.addHandler(console)

    return logger
