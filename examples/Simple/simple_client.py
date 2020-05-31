#!/usr/bin/python3

import logging
import numpy as np
from numpysocket import NumpySocket

logger = logging.getLogger('simple client')
logger.setLevel(logging.INFO)

logger.info("waiting for frame")
npSocket = NumpySocket()

npSocket.startClient(9999)
frame = npSocket.recieveNumpy()
logger.info("frame recieved")
logger.info(frame)

try:
    npSocket.endServer()
except OSError as err:
    logging.error("server already disconnected")
