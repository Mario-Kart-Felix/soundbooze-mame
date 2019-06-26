import time

import sys
import cv2
import mss
import numpy

subtractor = cv2.createBackgroundSubtractorMOG2(history=20, varThreshold=25, detectShadows=True)

def grab(width, height, left, top):

    with mss.mss() as sct:

        monitor = {"top": top, "left": left, "width": width, "height": height}

        while [ 1 ]:
            last_time = time.time()

            img = numpy.array(sct.grab(monitor))
            mask = subtractor.apply(img)

            # [shared - distributed] obstacles/threads detection

            #h = numpy.hsplit(mask, 2)
            #v = numpy.vsplit(h[1], 2)

            cv2.imshow("OpenCV/Numpy normal", mask)

            #print("fps: {}".format(1 / (time.time() - last_time)))

            # Press "q" to quit
            if cv2.waitKey(25) & 0xFF == ord("q"):
                cv2.destroyAllWindows()
                break

grab(int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]))
