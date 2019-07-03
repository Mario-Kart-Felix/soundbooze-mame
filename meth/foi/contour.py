import mss
import cv2
import time
import numpy

def contours(img):
    try:
        ret,thresh = cv2.threshold(img, 127, 255, 0)
        contours,hierarchy = cv2.findContours(thresh, 1, 2)
        return contours[0]
    except:
        pass

with mss.mss() as sct:

    full = {"top": 124, "left": 100, "width": 800, "height": 600}
    Z = numpy.array([])

    while [ 1 ]: 

        img = numpy.array(sct.grab(full))
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        cnt = contours(gray)

        if cnt is not None:
            l = len(cnt)
            w = numpy.where(Z == l)[0]
            if len(w) == 0:
                Z = numpy.append(Z, l)
                Z = numpy.unique(Z)
                cv2.imwrite('tmp/' + str(l) + "-" + str(time.time()) + '.png', img)

            '''
            if l >= numpy.percentile(Z, 50):
                print time.time(), l, Z
            '''

            '''
            for c in cnt:
                x = c.ravel()[0]
                y = c.ravel()[1]
                cv2.circle(img,(x,y), 4, (255,255,255), -1)
            '''
        '''
        cv2.imshow("OpenCV/Numpy normal", img)
        if cv2.waitKey(25) & 0xFF == ord("q"):
            cv2.destroyAllWindows()
            break
        '''
