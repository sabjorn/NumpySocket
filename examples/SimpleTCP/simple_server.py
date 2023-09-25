#!/usr/bin/python3
import logging

from numpysocket import NumpySocket

logging.basicConfig(level=logging.INFO)

with NumpySocket() as s:
    s.bind(("", 9999))
    s.listen()
    conn, addr = s.accept()
    with conn:
        logging.info(f"connected: {addr}")
        frame = conn.recv()

        logging.info("array received")
        logging.info(frame)

    logging.info(f"disconnected: {addr}")
