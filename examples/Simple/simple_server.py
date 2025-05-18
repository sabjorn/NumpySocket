#!/usr/bin/python3

import logging

from numpysocket import NumpySocket

logger = logging.getLogger("simple server")
logger.setLevel(logging.INFO)

with NumpySocket() as s:
    s.bind(("", 9999))
    s.listen()
    logger.info("Server listening on port 9999")
    conn, addr = s.accept()
    with conn:
        logger.info(f"connected: {addr}")
        while True:
            frame = conn.recv()
            if frame is None or (hasattr(frame, "size") and frame.size == 0):
                logger.info("Client disconnected")
                break
            logger.info("array received")
            logger.info(frame)
        logger.info(f"disconnected: {addr}")
