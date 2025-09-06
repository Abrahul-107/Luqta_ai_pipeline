import time
from app.core.logging_config import logger

def log_time(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        try:
            return func(*args, **kwargs)
        finally:
            elapsed = time.time() - start
            logger.info("⏱️ %s took %.3f seconds", func.__name__, elapsed)
    return wrapper
