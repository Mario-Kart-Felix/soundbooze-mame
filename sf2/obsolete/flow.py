import sys
import cv2
import mss
import time
import numpy
from scipy.stats import skew, kurtosis
from scipy.signal import find_peaks

from PIL import Image
from PIL import ImageFilter

def calcHistogram(img):

    #gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    num = numpy.prod(img.shape[:2])
    hist = cv2.calcHist([img], [0], None, [16], [0, 255]) / num
    s = skew(hist)
    k = kurtosis(hist)
    v = numpy.var(hist)
    hsum = numpy.sum(hist)/100.0
    m = (s + k + v + hsum) / 4
    return hsum, m 

def getFrame(width, height, left, top):
    with mss.mss() as sct:
        monitor = {"top": top, "left": left, "width": width, "height": height}
        frame = numpy.array(sct.grab(monitor))
        return frame

def grab(width, height, left, top):

    with mss.mss() as sct:

        monitor = {"top": top, "left": left, "width": width, "height": height}
        subtractor = cv2.createBackgroundSubtractorMOG2(history=20, varThreshold=25, detectShadows=True)

        feature_params = dict( maxCorners = 100,
                       qualityLevel = 0.3,
                       minDistance = 7,
                       blockSize = 7 )

        lk_params = dict( winSize  = (15,15),
                  maxLevel = 2,
                  criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))
        
        lcolor = (61,61,61)
        ccolor = (161,161,161)

        old_frame = getFrame(width, height, left, top)
        old_gray = cv2.cvtColor(old_frame, cv2.COLOR_BGR2GRAY)
        p0 = cv2.goodFeaturesToTrack(old_gray, mask = None, **feature_params)
        mask = numpy.zeros_like(old_frame)

        m = 0
        while [ 1 ]:

            frame = numpy.array(sct.grab(monitor))
            frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            p1, st, err = cv2.calcOpticalFlowPyrLK(old_gray, frame_gray, p0, None, **lk_params)

            if p1 is None:
                p1 = [[0, 0]]
            if st is None:
                st = [[0]]

            good_new = p1[st==1]
            good_old = p0[st==1]

            if len(good_new) == 0:
                good_new = [[0, 0]]
            if len(good_old) == 0:
                good_old = [[0, 0]]

            #blankify
            frame[:,:,0] = 0
            frame[:,:,1] = 0
            frame[:,:,2] = 0

            for i,(new,old) in enumerate(zip(good_new,good_old)):

                if new[0] == 0 and new[1] == 0:
                    break

                a,b = new.ravel()
                c,d = old.ravel()

                x = numpy.absolute(c-a)
                y  = numpy.absolute(d-b)

                if x != 0 and y != 0:

                    if y > 20 and y < 50:
                        print '[Incoming Danger]',
                        print str(time.time()),
                        print ("%.5f"% (x)),
                        print ("%.5f"% (y))

                    if x >= 0.05 and y >= 0.05:
                        mask = cv2.line(mask,(a,b),(c,d), lcolor, 1)
                        frame = cv2.circle(frame,(a,b),3,ccolor,-1)

            # getrealfps,sync ....
            if m % 60 == 0:
                mask = numpy.zeros_like(frame)

            m = m + 1

            img = cv2.add(frame,mask)

            cv2.imshow('frame',img)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                cv2.destroyAllWindows()
                quit = not quit
                break

            old_gray = frame_gray.copy()
            p0 = cv2.goodFeaturesToTrack(old_gray, mask = None, **feature_params)

            #Subtractor

            '''
            frame = numpy.array(sct.grab(monitor))
            sub = subtractor.apply(frame)
            blur = cv2.GaussianBlur(sub,(5,5),0)

            pil_img = Image.fromarray(blur)
            edge = numpy.array(pil_img.filter(ImageFilter.FIND_EDGES))
            edgecv = cv2.cvtColor(numpy.array(edge), cv2.COLOR_RGB2BGR)

            blursum = (numpy.sum(blur)/1000000.0)
            hsum, m = calcHistogram(blur)

            if m > 0:
                if blursum > 0.0 and blursum < 1.8:
                    H = numpy.hsplit(blur, 6)
                    Hsum = numpy.sum(H)/1000000.0
                    if Hsum < 1.0:

                        # mid

                        idx2sum = numpy.sum(H[2])/1000000.0
                        idx3sum = numpy.sum(H[3])/1000000.0

                        if (idx2sum > 0.0 and idx2sum < 1.0) and (idx3sum > 0.0 and idx3sum < 1.0):
                            print idx2sum, idx3sum

                        z = []
                        for h in H:
                            #print ("%.5f"% (numpy.sum(h)/1000000.0)),
                            z.append(numpy.sum(h)/1000000.0)

                        from scipy import stats
                        rs = stats.find_repeats(z)
                        print rs[0], rs[1]

                        cv2.imshow('2', H[2])
                        cv2.imshow('3', H[3])

                    #print ("%.5f"% (hsum)),
                    #print ("%.5f"% blursum)

            #cv2.imshow("Blur", blur)

            if cv2.waitKey(25) & 0xFF == ord("q"):
                cv2.destroyAllWindows()
                break
            '''

grab(540, 400, 107, 114)
#grab(540, 60, 112, 370)
