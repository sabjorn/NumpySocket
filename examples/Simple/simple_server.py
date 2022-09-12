#!/usr/bin/python3

import logging

from numpysocket import NumpySocket

logger = logging.getLogger('simple server')
logger.setLevel(logging.INFO)

with NumpySocket() as s:
    s.bind(('', 9999))
    s.listen()
    conn, addr = s.accept()
    with conn:
        logger.info(f"connected: {addr}")
        frame = conn.recv()

        logger.info("array received")
        logger.info(frame)

    logger.info(f"disconnected: {addr}")

