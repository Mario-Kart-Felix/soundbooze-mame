import mss
import cv2
import time
import numpy
import hashlib 
import multiprocessing

from ryu import *
from rb import *
from archive import *

BLOOD  = [2744512, 4089536, 745816 * 4]
RESUME = [1358640, 2623509]

class Image:

    def __init__(self, directory):
        self.directory = directory
        self.i = self.directory + '/i/'
        self.x = self.directory + '/x/'
        self.c = 0

    def dump(self, x, i):
        cv2.imwrite(self.i + str(c) + '.png', numpy.reshape(x, (50,100)))
        cv2.imwrite(self.x + str(c) + '.png', numpy.reshape(i, (50,100)))
        self.c += 1

    def hash(self, img):
        result = hashlib.md5(str(img.ravel()).encode()) 
        return result.hexdigest()

    def minsubtract(self, A, x): 

        def _graysub(img_a, img_b):
            s = numpy.sum((img_a - img_b))/100000000.0
            return s 

        ms = numpy.iinfo('i').max
        t = time.time()
        img = None
        for a in A:
            for i in a:
                s = _graysub(x, i)
                if s < ms:
                    ms = s
                    img = i

        return ms, time.time() - t, self.hash(img)

def risk(r, ev, ns):

    def _run(r):
        ns.value = True
        ev.set()

        '''
        if r == 0:
        elif r == 1:
        elif r == 2:
        elif r == 3:
        '''

        ns.value = False
        ev.set()

    z = False

    try:
        z = ns.value
        if not z:
            _run(r)

    except Exception, err:
        _run(r)
        pass

    ev.wait()

def advantage(a, ev, ns):

    def _run(a):
        ns.value = True
        ev.set()

        '''
        if a == 0:
        elif a == 1:
        elif a == 2:
        elif a == 3:
        '''

        ns.value = False
        ev.set()

    z = False

    try:
        z = ns.value
        if not z:
            _run(a)

    except Exception, err:
        _run(a)
        pass

    ev.wait()

def inference(x):

    if len(PENALTY) > 0:
        msp, t, ip = image.minsubtract(PENALTY, x) 
        rp = numpy.random.choice(4, 1, p=[0.2, 0.3, 0.1, 0.4])
        HP[ip] = rp

    if len(REWARD) > 0:
        msr, t, ir = image.minsubtract(REWARD, x) 
        rr = numpy.random.choice(4, 1, p=[0.2, 0.3, 0.1, 0.4])
        HR[ir] = rr 

    if msp < msr:
        print("[R] %.5f (%.5f) %s [%d] [%.5f, %.5f]" %(msp, t, ip, rp, (0.4089536-sumb1/10000000.0), (0.4089536-sumb2/10000000.0)))  
        z = ['R', ip, rp, 0.4089536-sumb2/10000000.0]
        ZEQ.append(z)
        r = multiprocessing.Process(target=risk, args=(rp,ev,ns)) 
        r.start()

    elif msp > msr: 
        print("[A] %.5f (%.5f) %s [%d] [%.5f, %.5f]" %(msr, t, ir, rr, (0.4089536-sumb1/10000000.0), (0.4089536-sumb2/10000000.0)))  
        z = ['A', ir, rr, 0.4089536-sumb2/10000000.0]
        ZEQ.append(z)
        a = multiprocessing.Process(target=advantage, args=(rr,ev,ns)) 
        a.start() 

with mss.mss() as sct:

    border = 24
    blood = {"top": 100+border, "left": 100, "width": 800, "height":600}
    scene = {"top": 240+border, "left": 100, "width": 800, "height":480}

    startGame = False

    ryu = RYU()
    mgr = multiprocessing.Manager()
    ns = mgr.Namespace()
    ev = multiprocessing.Event()

    korb = RingBuffer(4)
    archive = Archive()
    image = Image('/tmp/')

    PENALTY, REWARD = [], []
    HP, HR, ZEQ = {}, {}, []

    while [ 1 ]:

        p1 = numpy.array(sct.grab(blood))
        p2 = p1.copy()

        b1 = p1[60:78, 68:364]
        b2 = p2[60:78, 68+366:364+366]
        ko = p1[60:80, 378:424]

        sumb1, sumb2, kosum = numpy.sum(b1), numpy.sum(b2), numpy.sum(ko)
        korb.append(kosum)

        if sumb1 >= BLOOD[0] and sumb1 <= BLOOD[1]:

            if startGame:
                x = cv2.resize(numpy.array(sct.grab(scene))[:,:,0],(100,50)).ravel()
                inference(x)
                
            z = korb.get()
            zsum = 0
            try:
                zsum = numpy.sum(z)
            except:
                pass

            if sumb1 == BLOOD[1] and sumb2 == BLOOD[1] and not startGame:
                print '[Start]'
                startGame = True
                tp, tr = archive.load(numpy.array(sct.grab(scene))[:,:,0])
                PENALTY, REWARD = archive.P, archive.R
                print '[PENALTY]:', len(PENALTY), '('+str(tp)+')'
                print '[REWARD]:', len(REWARD),   '('+str(tr)+')'
                time.sleep(1)

            elif sumb1 == BLOOD[0] and zsum == BLOOD[2]:
                print 'P1 [KO]'
                startGame = False
                time.sleep(1)

            elif sumb2 == BLOOD[0] and zsum == BLOOD[2]:
                print 'P2 [KO]'
                startGame = False
                time.sleep(1)

        elif sumb1 == RESUME[0]:
            ryu.insertcoin()
        
        elif sumb1 == RESUME[1]:
            ryu.select()
