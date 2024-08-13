import logging

def setup_logger(log_level, log_file):
    logging.basicConfig(
        filename=log_file,
        level=getattr(logging, log_level.upper()),
        format='%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

def get_logger(name):
    return logging.getLogger(name)