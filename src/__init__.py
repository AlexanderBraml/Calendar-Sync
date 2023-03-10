import logging

log_file = 'calendar-sync.log'


def setup_logger(name, log_level):
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(module)s:%(lineno)s %(message)s', '%Y-%m-%d %H:%M:%S')

    if log_file:
        handler = logging.FileHandler(log_file, mode='a')
    else:
        handler = logging.StreamHandler()
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(log_level)
    logger.addHandler(handler)
    return logger


setup_logger('calendar_sync', logging.INFO)
