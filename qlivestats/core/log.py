import logging
import logging.handlers

LOG_FILENAME = '/tmp/qlivestats.out.log'

# Set up a specific logger with our desired output level
logger = logging.getLogger("qlivestats")
logger.setLevel(logging.DEBUG)

# Add the log message handler to the logger
handler = logging.handlers.RotatingFileHandler(
                  LOG_FILENAME, maxBytes=20, backupCount=5)

logger.addHandler(handler)

def setInteractiveLogging():
    handlerStdout = logging.StreamHandler(stream=sys.stdout)
    handlerStdout.setLevel(logging.DEBUG)
    logger.addHandler(handlerStdout)

