#!/usr/bin/python3

import os
import logging
import socket

from numpysocket import NumpySocket

logger = logging.getLogger("unix socket server")
logger.setLevel(logging.INFO)

socket_path = "/tmp/socket"

# Ensure the socket does not already exist
try:
    os.unlink(socket_path)
except OSError:
    if os.path.exists(socket_path):
        raise

with NumpySocket(socket.AF_UNIX, socket.SOCK_STREAM) as s:
    s.bind(socket_path)
    s.listen()
    conn, addr = s.accept()
    with conn:
        logger.info(f"connected: {addr}")
        frame = conn.recv()

        logger.info("array received")
        logger.info(frame)

    logger.info(f"disconnected: {addr}")
