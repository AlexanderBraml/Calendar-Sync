import logging


def setup_logger(name, log_level):
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(module)s:%(lineno)s %(message)s', '%Y-%m-%d %H:%M:%S')

    handler = logging.StreamHandler()
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(log_level)
    logger.addHandler(handler)
    return logger


setup_logger('calendar_sync', logging.INFO)
