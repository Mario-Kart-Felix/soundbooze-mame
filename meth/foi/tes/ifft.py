import sys
import cv2
import mss
import numpy

with mss.mss() as sct:

    monitor = {"top": 124, "left": 100, "width": 800, "height": 600}

    while [ 1 ]:

        img = numpy.array(sct.grab(monitor))
        img = cv2.resize(img, (400,300))

        img[:,:,1] = 0
        img[:,:,2] = 0
        img[img < 255] = 0

        f = numpy.fft.fft2(img)
        fshift = numpy.fft.fftshift(f)

        rows, cols, _ = img.shape
        crow,ccol = rows/2 , cols/2
        fshift[crow-30:crow+30, ccol-30:ccol+30] = 0
        f_ishift = numpy.fft.ifftshift(fshift)
        img_back = numpy.fft.ifft2(f_ishift)
        img_back = numpy.abs(img_back)
            
        cv2.imshow("torcs", img_back)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            cv2.destroyAllWindows()
            break
