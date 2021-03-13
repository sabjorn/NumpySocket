#!/usr/bin/python3

import logging
import numpy as np
from numpysocket import NumpySocket

logger = logging.getLogger('simple server')
logger.setLevel(logging.INFO)

npSocket = NumpySocket()

logger.info("starting server, waiting for client")
npSocket.startServer(9999)

frame = npSocket.recieve()
logger.info("array recieved:")
logger.info(frame)

logger.info("closing connection")
try:
    npSocket.close()
except OSError as err:
    logging.error("server already disconnected")
