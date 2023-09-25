#!/usr/bin/python3
import logging
import socket

logging.basicConfig(level=logging.INFO)

UDP_IP = "127.0.0.1"
UDP_PORT = 5005
MESSAGE = b"Hello, World!"

logging.info("UDP target IP: %s" % UDP_IP)
logging.info("UDP target port: %s" % UDP_PORT)
logging.info("message: %s" % MESSAGE)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # Internet  # UDP
sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))
