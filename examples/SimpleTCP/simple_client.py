#!/usr/bin/python3

import logging
import numpy as np
from numpysocket import NumpySocket

logging.basicConfig(level=logging.INFO)


with NumpySocket() as s:
    s.connect(("localhost", 9999))

    logging.info("sending numpy array:")
    frame = np.arange(1000)
    s.sendall(frame)
