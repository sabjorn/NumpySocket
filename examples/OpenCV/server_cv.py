from numpysocket import NumpySocket
import cv2
from scipy.misc import imresize

host_ip = 'localhost'  # change me
cap = cv2.VideoCapture(0)
npSocket = NumpySocket()
npSocket.startServer(host_ip, 9999)

# Read until video is completed
while(cap.isOpened()):
    ret, frame = cap.read()
    ref_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    frame_resize = imresize(ref_frame, .5)
    if ret is True:
        npSocket.sendNumpy(frame_resize)
    else:
        break
# When everything done, release the video capture object
npSocket.endServer()
cap.release()
