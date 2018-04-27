import logging

import logging_config

logging_config.init()
logger = logging.getLogger("Test")

logger.info("This is Info")
logger.warning("This is warning")
logger.error("This is error")
logger.critical("This is critical")
logger.debug("This is debug")
