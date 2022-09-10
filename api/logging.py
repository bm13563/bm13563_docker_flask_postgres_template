from logging import Formatter, StreamHandler, getLogger, DEBUG, INFO, WARNING, ERROR

class CustomFormatter(Formatter):
    """Logging Formatter to add colors and alter format"""

    level_suffix = (
        "[%(asctime)s] %(levelname)s in %(filename)s:%(lineno)d: %(message)s"
        + "\x1b[0m"
    )

    FORMATS = {
        DEBUG: "\033[92m" + level_suffix,
        INFO: "\033[94m" + level_suffix,
        WARNING: "\033[93m" + level_suffix,
        ERROR: "\033[91m" + level_suffix,
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = Formatter(log_fmt)
        return formatter.format(record)


def get_logger(name="api", level=DEBUG):
    logger = getLogger(name)
    logger.setLevel(level)
    if not logger.handlers:
        log_handler = StreamHandler()
        log_handler.setFormatter(CustomFormatter())
        logger.addHandler(log_handler)
    return logger
