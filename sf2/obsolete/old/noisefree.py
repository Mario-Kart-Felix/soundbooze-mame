import numpy
import cv2
import mss
import time

from skimage.measure import compare_ssim

def similar(img_a, img_b):
    sim, _ = compare_ssim(numpy.array(img_a), numpy.array(img_b), full=True)
    return sim

def threshold(gray):
    ret, thresh = cv2.threshold(gray,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
    return thresh

with mss.mss() as sct:

    border = 24
    L = {"top": 610+border, "left": 100, "width": 800, "height":104-border}
    prevstate = numpy.array(sct.grab(L))[:,:,0]

    while [ 1 ]:
        state = numpy.array(sct.grab(L))[:,:,0]
        s = similar(prevstate, state) #resize
        prevstate = state

        #rgb4 = numpy.array(sct.grab(L))
        #uc3 = numpy.array(sct.grab(L))[:,:,:3]

        cv2.imshow('L', threshold(state))
        k = cv2.waitKey(20) & 0xff
        if k == 27:
            break
    
