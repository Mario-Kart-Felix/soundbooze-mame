import sys
import cv2
import mss
import numpy

with mss.mss() as sct:

    monitor = {"top": 124, "left": 100, "width": 800, "height": 600}

    while [ 1 ]:

        img = numpy.array(sct.grab(monitor))

        img[:,:,2] = 0
        img[img < 255] = 0

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        f = numpy.fft.fft2(gray)
        fshift = numpy.fft.fftshift(f)
        magnitude_spectrum = 20*numpy.log(numpy.abs(fshift))
        magnitude_spectrum = numpy.asarray(magnitude_spectrum, dtype=numpy.uint8)
        #img_and_magnitude = numpy.concatenate((gray, magnitude_spectrum), axis=1)

    
        ''''
        center = magnitude_spectrum[290:310, 390:410]
        z = numpy.sum(center)/100000.0
        if z >= 0.9:
            print z
        '''

        cv2.imshow("torcs", magnitude_spectrum)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            cv2.destroyAllWindows()
            break
