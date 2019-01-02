import logging
from pathlib import Path


def Logger(name):
    """
    Issue with initialization.

    The logging doesn't seem to work if we don't make atleast one
    call to basicConfig() (maybe i'm missing something there).

    So only one call is made to basicConfig() because
    basicConfig() doesn't add a handler if the rootLogger already has
    one which puts us in a unwanted situation.

    If we call basicConfig() in every call then every module will try to
    have a handler to log to files but basicConfig() would simply
    oversee it and not return the cache handler which will end us
    up with a log full of CACHE writted over.

    ---------------------------------------------------
    Current solution: Broken.

    I have tried to make the call to basicConfig() just once.
    This once is done when no handlers are present in the rootLogger,
    i:e done by cache.

    After that every call will work properly.
    However after that as we log something to the file, it is accompanied
    by another line with same info but done by the cache handler.

    It seems like every other logger (other than cache) has 3 handlers.
    One: For console: Working perfectly.
    Two: Filehandler: Working perfectly.
    Third: The filehandler of cache since it was called by basicConfig()

    I have tried to check the number of handlers in every logger,
    they report 2 for each except for cache which simply means if the
    handler is added by basicConfig() then it is not considered a handler.

    -------------------------------------------------
    Possible patch?
    Try to stop basicConfig() from addding its handler to all other loggers.
    """
    logger = logging.getLogger(name)

    log_path = Path('~/.playx/logs/log.cat').expanduser()

    log_format = "[{}]: %(message)s".format(name)
    log_format_file = "[{}]-[%(asctime)s]: %(message)s".format(name.upper())

    if not len(logging.getLogger().handlers):
        logging.basicConfig(level=logging.INFO,
                            filename=log_path,
                            format=log_format_file
                            )
        logging.info("basicConfig() called by {}".format(name))
    #else:
    filehandler = logging.FileHandler(log_path)
    filehandler.setLevel(logging.INFO)
    filehandler.setFormatter(logging.Formatter(log_format_file))
    logger.addHandler(filehandler)

    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    console.setFormatter(logging.Formatter(log_format))
    logger.addHandler(console)

    if len(logger.handlers) == 1:
        # In case of cache only one handler is present since the other
        # one is created by basicConfig()
        # Lets just add another one by filehandler
        filehandler = logging.FileHandler(log_path)
        filehandler.setLevel(logging.INFO)
        filehandler.setFormatter(logging.Formatter(log_format_file))
        logger.addHandler(filehandler)

    logging.info("{}: Handlers in root".format(len(logging.getLogger().handlers)))
    logging.info('{}: Handlers present in {}'.format(len(logger.handlers), name))

    return logger
