#!/usr/bin/python3

import logging
import socket

import numpy as np

from numpysocket import NumpySocket


logger = logging.getLogger("unix socket client")
logger.setLevel(logging.INFO)

socket_path = "/tmp/socket"

with NumpySocket(socket.AF_UNIX, socket.SOCK_STREAM) as s:
    s.connect(socket_path)

    logger.info("sending numpy array:")
    frame = np.arange(1000)
    s.sendall(frame)
