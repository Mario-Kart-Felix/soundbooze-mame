import cv2
import mss
import numpy 

class BLOOD:

    def __init__(self):

        self.p1 = {"top": 164, "left": 130, "width": 350, "height": 44}
        self.p2 = {"top": 164, "left": 530, "width": 350, "height": 44}

        self.ko = 3280320

        self.lower_green = numpy.array([50,100,100])
        self.upper_green = numpy.array([60,255,255])
        self.lower_white = numpy.array([0,0,255])
        self.upper_white = numpy.array([0,0,255])

    def compute(self):

        bloodp1 = numpy.array(sct.grab(blood.p1))
        bloodp2 = numpy.array(sct.grab(blood.p2))

        hsv1 = cv2.cvtColor(bloodp1, cv2.COLOR_BGR2HSV)
        hsv2 = cv2.cvtColor(bloodp2, cv2.COLOR_BGR2HSV)

        maskgreen1 = cv2.inRange(hsv1, blood.lower_green, blood.upper_green)
        maskwhite1 = cv2.inRange(hsv1, blood.lower_white, blood.upper_white)
        maskgreen2 = cv2.inRange(hsv2, blood.lower_green, blood.upper_green)
        maskwhite2 = cv2.inRange(hsv2, blood.lower_white, blood.upper_white)

        resgreen1 = cv2.bitwise_and(bloodp1, bloodp1, mask= maskgreen1)
        reswhite1 = cv2.bitwise_and(bloodp1, bloodp1, mask= maskwhite1)
        resgreen2 = cv2.bitwise_and(bloodp2, bloodp2, mask= maskgreen2)
        reswhite2 = cv2.bitwise_and(bloodp2, bloodp2, mask= maskwhite2)

        sumrg1, sumrg2 = numpy.sum(resgreen1), numpy.sum(resgreen2)
        sumrw1, sumrw2 = numpy.sum(reswhite1), numpy.sum(reswhite2)

        p1 = sumrg1 if sumrg1 > sumrw1 else sumrw1
        p2 = sumrg2 if sumrg2 > sumrw2 else sumrw2

        return p1, p2

with mss.mss() as sct:

    blood = BLOOD()

    while [ 1 ]:

        p1, p2 = blood.compute()

        if p1 == blood.ko:
            print 'P1 [KO]'
        elif p2 == blood.ko:
            print 'P2 [KO]'

        print p1, '-', p2
