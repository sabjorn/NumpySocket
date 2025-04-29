#!/usr/bin/env python3
from typing import Any
from io import BytesIO

import unittest
from unittest.mock import patch
import numpy as np

from numpysocket import NumpySocket

import socket


class TestNumpySocket(unittest.TestCase):
    def setUp(self) -> None:
        self.test_array = np.array([[1, 2, 3], [4, 5, 6]])
        self.npsocket = NumpySocket()

    @patch.object(socket.socket, "sendall")
    def test_sendall(self, mock_sendall: Any) -> None:
        """Test that sendall properly formats and sends numpy arrays"""
        self.npsocket.sendall(self.test_array)

        mock_sendall.assert_called_once()
        sent_bytes = mock_sendall.call_args[0][0]
        header, data = sent_bytes.split(b":", 1)
        length = int(header)
        self.assertEqual(length, len(data))
        reconstructed = np.load(BytesIO(data), allow_pickle=True)["frame"]
        np.testing.assert_array_equal(reconstructed, self.test_array)

    @patch.object(socket.socket, "recv")
    def test_recv(self, mock_recv: Any) -> None:
        """Test that recv properly reconstructs numpy arrays from received bytes"""
        f = BytesIO()
        np.savez(f, frame=self.test_array)
        packet = f.getvalue()
        header = f"{len(packet)}:".encode()
        mock_recv.side_effect = [
            header,
            packet[: len(packet) // 2],
            packet[len(packet) // 2 :],
        ]

        result = self.npsocket.recv()

        np.testing.assert_array_equal(result, self.test_array)
        self.assertEqual(mock_recv.call_count, 3)

    @patch.object(socket.socket, "recv")
    def test_recv_empty(self, mock_recv: Any) -> None:
        """Test that recv handles empty data correctly"""
        mock_recv.return_value = b""

        result = self.npsocket.recv()

        self.assertTrue(np.array_equal(result, np.array([])))
        mock_recv.assert_called_once()

    @patch.object(socket.socket, "_accept")
    def test_accept(self, mock_accept: Any) -> None:
        """Test that accept returns a NumpySocket instance"""
        mock_accept.return_value = (42, ("127.0.0.1", 8888))

        with patch("socket.socket.__init__", return_value=None):
            client_socket, addr = self.npsocket.accept()

            self.assertIsInstance(client_socket, NumpySocket)
            self.assertEqual(addr, ("127.0.0.1", 8888))


if __name__ == "__main__":
    unittest.main()
