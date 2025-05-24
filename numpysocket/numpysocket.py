#!/usr/bin/env python3

from io import BytesIO
import logging
import socket
from typing import Any, Union, Tuple

import numpy as np


class NumpySocket(socket.socket):
    def sendall(self, frame: np.ndarray) -> None:  # type: ignore[override]
        out = self.__pack_frame(frame)
        super().sendall(out)
        logging.debug("frame sent")

    def recv(self, bufsize: int = 1024) -> np.ndarray:  # type: ignore[override]
        length = None
        frame_buffer = bytearray()

        while True:
            receive_size = bufsize
            if length is not None:
                remaining = length - len(frame_buffer)
                receive_size = min(bufsize, remaining)
                logging.debug(
                    f"Receiving {receive_size} of {remaining} remaining bytes"
                )

            data = super().recv(receive_size)
            if len(data) == 0:
                return np.array([])

            frame_buffer += data
            if length is None:
                if b":" not in frame_buffer:
                    continue
                header, _, data = frame_buffer.partition(b":")
                try:
                    length = int(header.decode())
                    frame_buffer = data
                except ValueError:
                    logging.error("Invalid header format")
                    return np.array([])

            if len(frame_buffer) < length:
                continue

            frame_data = frame_buffer[:length]

            try:
                frame = np.load(BytesIO(frame_data), allow_pickle=True)["frame"]
                logging.debug("Frame received")
                return frame
            except Exception as e:
                logging.error(f"Error parsing frame: {e}")
                return np.array([])

    def accept(self) -> Tuple["NumpySocket", Union[Tuple[str, int], Tuple[Any, ...]]]:
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
