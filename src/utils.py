import os
from logging.config import dictConfig


# Logging
def setup_logs(logname):
    """
    Sets up logging
    :param logname: base name of log files
    :type logname: str
    :return:
    """

    if not os.path.isdir('logs'):
        os.mkdir('logs')

    dictConfig({
        'version': 1,
        'formatters': {'default': {
            'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
        }},
        'handlers': {'file': {
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': 'logs/{}.log'.format(logname),
            'formatter': 'default',
            'backupCount': 5,
            'when': 'midnight',
            'interval': 1
        }},
        'root': {
            'level': 'INFO',
            'handlers': ['file']
        }
    })


# data


if __name__ == "__main__":
    pass
