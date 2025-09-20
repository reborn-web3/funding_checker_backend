import sys
from loguru import logger
import logging
import urllib3


log_format = (
    "<light-blue>[</light-blue><yellow>{time:HH:mm:ss}</yellow><light-blue>]</light-blue> | "
    "<level>{level: <8}</level> | "
    "<cyan>{file}:{line}</cyan> | "
    "<level>{message}</level>"
)

class InterceptHandler(logging.Handler):
    """Перехватчик стандартных логов под loguru."""
    def emit(self, record):
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno
        logger.opt(depth=6, exception=record.exc_info).log(level, record.getMessage())


def configure_logging():
    urllib3.disable_warnings()
    logger.remove()
    
    logger.add(
        sys.stdout,
        colorize=True,
        format=log_format,
        level="INFO",
    )
    logger.add(
        "logs/app.log",
        rotation="10 MB",
        retention="1 month",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {name}:{line} - {message}",
        level="INFO",
        enqueue=True,
    )
    
    logging.basicConfig(handlers=[InterceptHandler()], level=0, force=True)

    return logger
