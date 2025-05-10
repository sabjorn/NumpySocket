#!/usr/bin/python3

import logging
import numpy as np
from numpysocket.numpysocket import NumpySocket


logger = logging.getLogger("simple client")
logger.setLevel(logging.INFO)

with NumpySocket() as s:
    s.connect(("localhost", 9998))

    logger.info("sending numpy array:")
    frame = np.arange(1000)
    s.sendall(frame)

    frame = np.array([6, 7, 8, 9, 1, 2, 3])
    s.sendall(frame)

    arr = s.recv()
    logger.info("array:")
    logger.info(arr)
