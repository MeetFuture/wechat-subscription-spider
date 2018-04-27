import logging
import logging.config
import os

default = os.path.join(os.path.dirname(__file__), 'logging.conf')

print("logging config exists:", os.path.exists(default), " File:", default)
if os.path.exists(default):
    logging.config.fileConfig(default)
    logging.getLogger(__name__).info("logger init cofig file [%s] success", default)
else:
    logging.basicConfig(level=logging.INFO,
                        format="%(asctime)s-%(msecs)s %(name)s P:%(process)s %(threadName)s [%(levelname)s] :%(message)s",
                        datefmt="%H:%M:%S",
                        style="")
    logging.getLogger(__name__).info("logger init basicConfig")


# ---------------------------------------------------------------------------
# 日志配置 确保第一个 import 引入
# ---------------------------------------------------------------------------
def init():
    logging.getLogger(__name__).info("Ensure logging_config is first import")
    return None
