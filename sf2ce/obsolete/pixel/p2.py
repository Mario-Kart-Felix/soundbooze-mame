import sys
import cv2
import mss
import numpy as np

left  = 156 + 248
top = 178
width = 197
height = 12

def getFrame():
    with mss.mss() as sct:
        monitor = {"top": top, "left": left, "width": width, "height": height}
        frame = np.array(sct.grab(monitor))
        return frame

prev = 0
while True:
    frame = getFrame()
    b = frame[:, :, 0]
    g = frame[:, :, 1]

    ssum = np.sum(b.ravel()) + np.sum(g.ravel())
    current = ((float(ssum)))
    sub = np.sqrt(prev - current)
    if current != prev:
        print '[P2] Hit: ' + str(sub) 
    prev = current

    if len(sys.argv) == 2:
        cv2.imshow("debug", frame)

        if cv2.waitKey(25) & 0xFF == ord("q"):
            cv2.destroyAllWindows()
            break

cv2.destroyAllWindows()
