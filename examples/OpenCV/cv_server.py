from numpysocket import NumpySocket
import cv2

cap = cv2.VideoCapture(0)
npSocket = NumpySocket()
npSocket.startServer(9999)

# Read until video is completed
while(cap.isOpened()):
    ret, frame = cap.read()
    ref_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    frame_resize = ref_frame[::2, ::2]
    if ret is True:
        try:
            npSocket.send(frame_resize)
        except:
            break
    else:
        break
# When everything done, release the video capture object
npSocket.close()
cap.release()
