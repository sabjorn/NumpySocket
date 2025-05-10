#!/usr/bin/python3

import logging
import numpy as np
from numpysocket.numpysocket import NumpySocket

logger = logging.getLogger("simple server")
logger.setLevel(logging.INFO)

with NumpySocket() as s:
    s.bind(("", 9998))
    s.listen()
    conn, addr = s.accept()
    with conn:
        logger.info(f"connected: {addr}")

        frame = conn.recv()
        logger.info("array received")
        logger.info(frame)

        frame = conn.recv()
        logger.info("array received")
        logger.info(frame)

        conn.sendall(np.array([1, 2, 3]))

    logger.info(f"disconnected: {addr}")
