from log_config import *


logger = configure_logging()

logger.debug("Подробности для разработчика")
logger.info("Всё прошло успешно")
logger.error("Что-то пошло не так!")