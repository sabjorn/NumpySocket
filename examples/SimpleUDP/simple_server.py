#!/usr/bin/python3

import logging
import socket

logging.basicConfig(level=logging.INFO)

UDP_IP = "127.0.0.1"
UDP_PORT = 5005

logging.info("starting server")
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # Internet  # UDP
sock.bind((UDP_IP, UDP_PORT))

while True:
    data, addr = sock.recvfrom(1024)  # buffer size is 1024 bytes
    logging.info("received message: %s" % data)
