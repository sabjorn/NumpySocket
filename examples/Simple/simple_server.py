#!/usr/bin/python3

import logging
from time import sleep
import numpy as np
from numpysocket import NumpySocket

logger = logging.getLogger('simple server')
logger.setLevel(logging.INFO)

host_ip = 'localhost'  # change me

npSocket = NumpySocket()
while(True):
    try:
        npSocket.startServer(host_ip, 9999)
        break
    except:
        logger.warning("connection failed, trying again.")
        sleep(1)
        continue

frame = np.arange(1000)
logger.info("sending frame: ")
logger.info(frame)
npSocket.sendNumpy(frame)

try:
    npSocket.endServer()
except OSError as err:
    logging.error("client already disconnected")
