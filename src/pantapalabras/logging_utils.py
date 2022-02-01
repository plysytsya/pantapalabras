import logging


def get_logger(name=None, level=logging.INFO):
    """Create a custom logger with default log-level INFO. Logger is named after this py-file if no name provided."""
    name = name or "pantapalabras"
    logger = logging.getLogger(name)
    if logger.hasHandlers():
        logger.handlers.clear()
    log_format = logging.Formatter("%(asctime)s : %(levelname)s : %(name)s : %(message)s")
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(log_format)
    logger.addHandler(stream_handler)
    logger.setLevel(level)
    logger.propagate = False
    logger.info("Initialized logger")
    return logger
