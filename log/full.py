import os
import sys
import mss
import cv2
import time
import numpy

from info import *

def init(d):

    i = Info()

    directory = d 
    session = i.uniq() + '-full'
    fullpath = directory + '/' + session + '/'

    if not os.path.exists(fullpath):
        os.mkdir(fullpath)

    fi = open(fullpath + 'info.txt', "w+")
    fi.write("INFO: %s\r\n" % i.info())
    fi.write("CONSTANT: %s\r\n" % i.constant())
    fi.write("UNIQ: %s\r\n" % i.uniq())
    fi.write("SCREEN: %s\r\n" % i.screen())
    fi.close()

    return fullpath

def mksubdir(fd):
    if not os.path.exists(fd):
        os.mkdir(fd)

def flushtoramdisk(m, fullpath, img):
    cv2.imwrite(fullpath + str(m-1) + '/' + str(time.time()) + '.png', img)

with mss.mss() as sct:

    fullpath = init(sys.argv[1]) 

    M = {}
    for num, monitor in enumerate(sct.monitors[1:], 1):
        M[num] = monitor

    for m in M:
        print 'Monitor #'+str(m-1), M[m]
        mksubdir(fullpath + str(m-1))

    while [ 1 ]: 

        last_time = time.time()

        for m in M:
            img = numpy.array(sct.grab(M[m]))
            flushtoramdisk(m, fullpath, img)

        print("fps: {}".format(1 / (time.time() - last_time)))
