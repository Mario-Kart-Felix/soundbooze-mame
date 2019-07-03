import mss
import cv2
import time
import numpy
import matplotlib.pyplot as plt

def shift_dft(src, dst):

    if src is dst:
        ret = numpy.empty(src.shape, src.dtype)
    else:
        ret = dst

    h, w = src.shape[:2]

    cx1 = cx2 = w // 2
    cy1 = cy2 = h // 2

    if w % 2 != 0:
        cx2 += 1
    if h % 2 != 0:
        cy2 += 1

    ret[h-cy1:, w-cx1:] = src[0:cy1 , 0:cx1 ] # q1 -> q3
    ret[0:cy2 , 0:cx2 ] = src[h-cy2:, w-cx2:] # q3 -> q1

    ret[0:cy2 , w-cx2:] = src[h-cy2:, 0:cx2 ] # q2 -> q4
    ret[h-cy1:, 0:cx1 ] = src[0:cy1 , w-cx1:] # q4 -> q2

    if src is dst:
        dst[:,:] = ret

    return dst

def logspectrum(frame):
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    h, w = frame.shape[:2]
    realInput = frame.astype(numpy.float64)
    dft_M = cv2.getOptimalDFTSize(w)
    dft_N = cv2.getOptimalDFTSize(h)
    dft_A = numpy.zeros((dft_N, dft_M, 2), dtype=numpy.float64)
    dft_A[:h, :w, 0] = realInput
    cv2.dft(dft_A, dst=dft_A, nonzeroRows=h)
    image_Re, image_Im = cv2.split(dft_A)
    magnitude = cv2.sqrt(image_Re**2.0 + image_Im**2.0)
    log_spectrum = cv2.log(1.0 + magnitude)
    return log_spectrum

def dft(frame):
    ls = logspectrum(frame)
    shift_dft(ls, ls)
    cv2.normalize(ls, ls, 0.0, 1.0, cv2.NORM_MINMAX)
    return ls

with mss.mss() as sct:

    full = {"top": 124, "left": 100, "width": 800, "height": 600}

    while [ 1 ]: 

        frame = numpy.array(sct.grab(full))
        ls = dft(frame)

        cv2.imshow("logspectrum", ls)
        if cv2.waitKey(25) & 0xFF == ord("q"):
            cv2.destroyAllWindows()
            break
