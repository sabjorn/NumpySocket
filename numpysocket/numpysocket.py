#!/usr/bin/env python3

from io import BytesIO
import logging
import socket
from typing import Any

import numpy as np


class NumpySocket(socket.socket):

    prev = None

    def sendall(self, frame: np.ndarray) -> None:  # type: ignore[override]
        out = self.__pack_frame(frame)

        super().sendall(out)
        logging.debug("frame sent")


    def recv(self, bufsize: int = 1024) -> np.ndarray:  # type: ignore[override]
        length = None
        frame_buffer = bytearray()
        frames = []
        while True:

            if self.prev == None or len(self.prev) == 0:
                data = super().recv(bufsize)
            else:
                data = self.prev
                self.prev = None

            if len(data) == 0:
                return np.array([])
            frame_buffer += data

            if length is None:
                if b":" not in frame_buffer:
                    assert(False) # throw error not np array
                length_str, ignored, frame_buffer = frame_buffer.partition(b":")
                length = int(length_str)

            if len(frame_buffer) >= length:
                frame = np.load(BytesIO(frame_buffer[:length]), allow_pickle=True)["frame"]
                self.prev = frame_buffer[length:]
                frames.append(frame)
                break

        frame = np.load(BytesIO(frame_buffer), allow_pickle=True)["frame"]
        logging.debug("frame received")
        return frame

    def accept(self):
        fd, addr = super()._accept()  # type: ignore
        sock = NumpySocket(super().family, super().type, super().proto, fileno=fd)

        if socket.getdefaulttimeout() is None and super().gettimeout():
            sock.setblocking(True)
        return sock, addr

    @staticmethod
    def __pack_frame(frame: np.ndarray) -> bytearray:
        f = BytesIO()
        np.savez(f, frame=frame)

        packet_size = len(f.getvalue())
        header = "{0}:".format(packet_size)
        header_bytes = bytes(header.encode())  # prepend length of array

        out = bytearray()
        out += header_bytes

        f.seek(0)
        out += f.read()
        return out