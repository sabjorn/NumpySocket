import unittest
import os
import socket
import threading
from typing import List
import numpy as np

from numpysocket import NumpySocket


class TestNumpySocketIntegration(unittest.TestCase):
    def setUp(self) -> None:
        self.socket_path = "/tmp/numpysocket_integration_test"

        try:
            os.unlink(self.socket_path)
        except OSError:
            pass

    def tearDown(self) -> None:
        try:
            os.unlink(self.socket_path)
        except OSError:
            pass

    def _run_socket_test(
        self, send_arrays: np.array, buffer_size: int = 1024
    ) -> List[np.array]:
        recv_count = len(send_arrays)

        received_arrays = []
        server_ready = threading.Event()
        server_done = threading.Event()

        def server_thread() -> None:
            with NumpySocket(socket.AF_UNIX, socket.SOCK_STREAM) as server:
                server.bind(self.socket_path)
                server.listen()
                server_ready.set()

                conn, _ = server.accept()
                with conn:
                    print("Server: Client connected")
                    for _ in range(recv_count):
                        frame = conn.recv(buffer_size)
                        received_arrays.append(frame)

                server_done.set()

        server = threading.Thread(target=server_thread)
        server.daemon = True
        server.start()

        server_ready.wait(timeout=5)

        with NumpySocket(socket.AF_UNIX, socket.SOCK_STREAM) as client:
            client.connect(self.socket_path)
            print("Client: Connected to server")

            for _, array in enumerate(send_arrays):
                client.sendall(array)

        server_done.wait(timeout=5)

        return received_arrays

    def test_small_array_large_buffer(self) -> None:
        test_array = np.array([[1, 2, 3], [4, 5, 6]])

        buffer_size = 4096

        received = self._run_socket_test([test_array], buffer_size=buffer_size)
        self.assertEqual(len(received), 1, "Should receive exactly one array")
        np.testing.assert_array_equal(received[0], test_array, "Arrays don't match")

    def test_small_array_small_buffer(self) -> None:
        test_array = np.array([[1, 2, 3], [4, 5, 6]])

        buffer_size = 32

        received = self._run_socket_test([test_array], buffer_size=buffer_size)

        self.assertEqual(len(received), 1, "Should receive exactly one array")
        np.testing.assert_array_equal(received[0], test_array, "Arrays don't match")

    def test_large_array_small_buffer(self) -> None:
        test_array = np.arange(900).reshape(30, 30)

        buffer_size = 64

        received = self._run_socket_test([test_array], buffer_size=buffer_size)

        self.assertEqual(len(received), 1, "Should receive exactly one array")
        np.testing.assert_array_equal(received[0], test_array, "Arrays don't match")

    def test_two_small_arrays(self) -> None:
        test_arrays = [
            np.array([[1, 2, 3], [4, 5, 6]]),
            np.array([[7, 8, 9], [10, 11, 12]]),
        ]

        received = self._run_socket_test(test_arrays, buffer_size=64)

        self.assertEqual(
            len(received),
            len(test_arrays),
            f"Should receive {len(test_arrays)} arrays, got {len(received)}",
        )

        for i, (sent, recv) in enumerate(zip(test_arrays, received)):
            np.testing.assert_array_equal(recv, sent, f"Array {i} doesn't match")

    def test_two_large_arrays(self) -> None:
        test_arrays = [
            np.arange(900).reshape(30, 30),
            np.arange(900, 1800).reshape(30, 30),
        ]

        received = self._run_socket_test(test_arrays, buffer_size=64)

        self.assertEqual(
            len(received),
            len(test_arrays),
            f"Should receive {len(test_arrays)} arrays, got {len(received)}",
        )

        for i, (sent, recv) in enumerate(zip(test_arrays, received)):
            np.testing.assert_array_equal(recv, sent, f"Array {i} doesn't match")

    def test_three_arrays_mixed_sizes(self) -> None:
        test_arrays = [
            np.array([[1, 2], [3, 4]]),
            np.arange(100).reshape(10, 10),
            np.arange(1000, 1900).reshape(30, 30),
        ]

        received = self._run_socket_test(test_arrays, buffer_size=64)

        self.assertEqual(
            len(received),
            len(test_arrays),
            f"Should receive {len(test_arrays)} arrays, got {len(received)}",
        )

        for i, (sent, recv) in enumerate(zip(test_arrays, received)):
            np.testing.assert_array_equal(recv, sent, f"Array {i} doesn't match")


if __name__ == "__main__":
    unittest.main()
