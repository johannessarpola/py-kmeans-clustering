import logging
from logging.handlers import RotatingFileHandler
from os import path, makedirs

class LoggerFactory(object):
    loggers = {}
    file_handler = None
    console_handler = None

    def __init__(self, dir='logs', fname='app.log', log_file_size = 5242880, backups_count = 5) -> None:
        logFormatter = logging.Formatter("%(asctime)s [%(name)s] [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")

        dest = path.join(dir, fname)

        self.file_handler = RotatingFileHandler(dest, maxBytes=log_file_size, backupCount=backups_count)
        self.file_handler.setFormatter(logFormatter)

        self.console_handler = logging.StreamHandler()
        self.console_handler.setFormatter(logFormatter)

        if not path.exists(dest):
            # TODO Test that this actually works
            self.instance(__name__).debug(f"Initializing logs folder to: {dest}")
            makedirs(dest)


    def instance(self, name, level = logging.DEBUG):
        if name in self.loggers:
            return self.loggers[name]
        else:
            logger = logging.getLogger(name)
            logger.setLevel(logging.DEBUG)
            logger.addHandler(self.console_handler)
            logger.addHandler(self.file_handler)
            self.loggers[name] = logger
            return logger

    def close(self):
        logging.shutdown()
