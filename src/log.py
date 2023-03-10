import logging


def setup_custom_logger(name):
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(module)s:%(lineno)s %(message)s', '%Y-%m-%d %H:%M:%S')

    handler = logging.StreamHandler()
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(handler)
    return logger
