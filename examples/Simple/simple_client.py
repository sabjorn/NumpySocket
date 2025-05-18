#!/usr/bin/python3

import logging
import numpy as np

from numpysocket import NumpySocket

logger = logging.getLogger("simple client")
logger.setLevel(logging.INFO)

with NumpySocket() as s:
    s.connect(("localhost", 9999))
    logger.info("Connecteed to localhost:9999")

    logger.info("sending numpy array:")
    frame = np.arange(1000)
    s.sendall(frame)

    logger.info("sending reversed numpy array:")
    frame = np.arange(1000, 0, -1)
    s.sendall(frame)

    logger.info("sending numpy array:")
    frame = np.arange(1000)
    s.sendall(frame)
