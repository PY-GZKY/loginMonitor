from loguru import logger
import time

def logging():
    logger.start(f'log/{time.strftime("%Y-%m-%d", time.localtime())}.log',format="{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}", encoding='utf-8')
    return logger

log_v = logging()
# log_v.debug("ok")
