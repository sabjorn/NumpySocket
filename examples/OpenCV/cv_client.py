#!/usr/bin/python3

from numpysocket import NumpySocket
import cv2

cap = cv2.VideoCapture(0)

with NumpySocket() as s:
    s.connect(("localhost", 9999))
    while cap.isOpened():
        ret, frame = cap.read()
        ref_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        frame_resize = ref_frame[::2, ::2]
        if ret is True:
            try:
                s.sendall(frame_resize)
            except Exception:
                break
        else:
            break
