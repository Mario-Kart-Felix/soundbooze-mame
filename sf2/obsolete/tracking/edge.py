import time

import sys
import cv2
import mss
import numpy

from PIL import Image
from PIL import ImageFilter

from pynput.keyboard import Key, Listener

import threading

key = ""

def keypress(Key):
    global key
    key = str(Key)

def gfg(): 

    with Listener(on_press = keypress) as listener:
        listener.join()
  
timer = threading.Timer(1.0, gfg) 
timer.start()

def describe(image, mask = None):
    hist = cv2.calcHist([image], [0, 1, 2], mask, [8,8,8], [0, 256, 0, 256, 0, 256])    
    cv2.normalize(hist, hist)    
    return hist.flatten() 

def grab(width, height, left, top):

    with mss.mss() as sct:

        monitor = {"top": top, "left": left, "width": width, "height": height}

        while [ 1 ]:
            last_time = time.time()

            img = numpy.array(sct.grab(monitor))
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            pil_img = Image.fromarray(gray)

            edge = numpy.array(pil_img.filter(ImageFilter.FIND_EDGES))
            edgecv = cv2.cvtColor(numpy.array(edge), cv2.COLOR_RGB2BGR)
            desc = describe(edgecv)

            sumdesc = 0
            for i in range(len(desc)):
                if desc[i] != 0:
                    sumdesc = sumdesc + desc[i]
                    print str(desc[i]) + ",",

            print str(sumdesc) + ", " + key

            cv2.imshow('videoUI', edgecv)

            #print("fps: {}".format(1 / (time.time() - last_time)))

            # Press "q" to quit
            if cv2.waitKey(25) & 0xFF == ord("q"):
                cv2.destroyAllWindows()
                break

grab(int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]))
