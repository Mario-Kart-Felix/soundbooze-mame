# -*- coding: utf-8 -*-

import cv2
import mss
import time
import numpy

with mss.mss() as sct:

    body = {"top": 284, "left": 100, "width": 800, "height": 300+24}

    while [ 1 ]:

        last_time = time.time()

        frame_b = numpy.array(sct.grab(body))

        red = frame_b.copy()
        green = frame_b.copy()
        blue = frame_b.copy()
        pink = frame_b.copy()

        # body

        red[:,:,0] = 0
        red[:,:,1] = 0
        red[red < 250] = 0

        green[:,:,0] = 0
        green[:,:,2] = 0
        green[green < 250] = 0

        blue[:,:,1] = 0
        blue[:,:,2] = 0
        blue[blue < 250] = 0

        pink[:,:,0] = 255
        pink[:,:,2] = 255

        gray = cv2.cvtColor(red, cv2.COLOR_BGR2GRAY)

        white = gray.copy()
        white[white > 0] = 255

        cv2.imshow("FF2 R", red)
        #cv2.imshow("FF2 G", green)
        #cv2.imshow("FF2 B", blue)
        #cv2.imshow("FF2 P", pink)
        #cv2.imshow("FF2 GR", gray)
        #cv2.imshow("FF2 W", white)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            cv2.destroyAllWindows()
            break

        print("fps: {}".format(1 / (time.time() - last_time)))
