import numpy as np
import cv2 as cv

def draw_hsv(flow):
    h, w = flow.shape[:2]
    fx, fy = flow[:,:,0], flow[:,:,1]
    ang = np.arctan2(fy, fx) + np.pi
    v = np.sqrt(fx*fx+fy*fy)
    hsv = np.zeros((h, w, 3), np.uint8)
    hsv[...,0] = ang*(180/np.pi/2)
    hsv[...,1] = 255
    hsv[...,2] = np.minimum(v*4, 255)
    bgr = cv.cvtColor(hsv, cv.COLOR_HSV2BGR)
    return bgr

def main():
    import sys
    try:
        fn = sys.argv[1]
    except IndexError:
        fn = 0

    cam = cv.VideoCapture(fn)

    ret, prev = cam.read()
    prevgray = cv.cvtColor(prev, cv.COLOR_BGR2GRAY)

    while True:
        ret, img = cam.read()
        gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

        flow = cv.calcOpticalFlowFarneback(prevgray, gray, None, 0.5, 3, 15, 3, 5, 1.2, 0)
        prevgray = gray

        hsv = draw_hsv(flow)
        hsvgray = cv.cvtColor(hsv, cv.COLOR_BGR2GRAY)

        cv.imshow('', img)
        cv.imshow('img', hsvgray)

        ch = cv.waitKey(20)
        if ch == 27:
            break

if __name__ == '__main__':
    print(__doc__)
    main()
    cv.destroyAllWindows()
