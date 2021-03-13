#!/usr/bin/env python3

import socket
import logging
import numpy as np
from io import BytesIO


class NumpySocket():
    def __init__(self):
        self.address = 0
        self.port = 0
        self.client_connection = self.client_address = None
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    def __del__(self):
        try:
            self.client_connection.shutdown(socket.SHUT_WR)
            self.socket.shutdown(socket.SHUT_WR)
        except (AttributeError, OSError):
            pass
        except Exception as e:
            logging.error("error when deleting socket", e)

        self.close()

    def startServer(self, port):
        self.address = ''
        self.port = port

        self.socket.bind((self.address, self.port))
        self.socket.listen(1)
        
        logging.debug("waiting for a connection")
        self.client_connection, self.client_address = self.socket.accept()
        logging.debug(f"connected to: {self.client_address[0]}")

    def startClient(self, address, port):
        self.address = address
        self.port = port
        try:
            self.socket.connect((self.address, self.port))
            logging.debug(f"Connected to {self.address} on port {self.port}")
        except socket.error as err:
            logging.error(f"Connection to {self.address} on port {self.port} failed")
            raise

    def close(self):
        try:
            self.client_connection.close()
        except AttributeError:
            pass
        self.client_connection = self.client_address = None
        self.socket.close()

    @staticmethod
    def __pack_frame(frame):
        f = BytesIO()
        np.savez(f, frame=frame)
        
        packet_size = len(f.getvalue())
        header = '{0}:'.format(packet_size)
        header = bytes(header.encode())  # prepend length of array

        out = bytearray()
        out += header

        f.seek(0)
        out += f.read()
        return out

    def send(self, frame):
        if not isinstance(frame, np.ndarray):
            raise TypeError("input frame is not a valid numpy array")

        out = self.__pack_frame(frame)

        socket = self.socket
        if(self.client_connection):
            socket = self.client_connection

        try:
            socket.sendall(out)
        except BrokenPipeError:
            logging.error("connection broken")
            raise

        logging.debug("frame sent")


    def recieve(self, socket_buffer_size=1024):
        socket = self.socket
        if(self.client_connection):
            socket = self.client_connection

        length = None
        frameBuffer = bytearray()
        while True:
            data = socket.recv(socket_buffer_size)
            frameBuffer += data
            if len(frameBuffer) == length:
                break
            while True:
                if length is None:
                    if b':' not in frameBuffer:
                        break
                    # remove the length bytes from the front of frameBuffer
                    # leave any remaining bytes in the frameBuffer!
                    length_str, ignored, frameBuffer = frameBuffer.partition(b':')
                    length = int(length_str)
                if len(frameBuffer) < length:
                    break
                # split off the full message from the remaining bytes
                # leave any remaining bytes in the frameBuffer!
                frameBuffer = frameBuffer[length:]
                length = None
                break
        
        frame = np.load(BytesIO(frameBuffer))['frame']
        logging.debug("frame received")
        return frame
