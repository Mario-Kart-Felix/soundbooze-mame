import mss
import cv2
import time
import numpy
import pickle
import hashlib 
import multiprocessing

from ryu import *
from rb import *
from archive import *

BLOOD  = [2744512, 4089536, 745816 * 4]
BONUS  = [3470538, 3066848, 3389388]
RESUME = [1358640, 2623509]

prevra = [0, 0, 0, 0] # prevrp1, prevrp2, prevap1, prevap2
ra     = [0, 0, 0, 0] # rp1, rp2, ap1, ap2                

hr, ha = multiprocessing.Manager(), multiprocessing.Manager()
HR, HA = hr.dict(), ha.dict()

class Image:

    def __init__(self, directory):
        self.directory = directory
        self.i = self.directory + '/i/'
        self.x = self.directory + '/x/'
        self.c = 0

    def dump(self, x, i):
        cv2.imwrite(self.x + str(self.c) + '.png', numpy.reshape(x, (50,100)))
        cv2.imwrite(self.i + str(self.c) + '.png', numpy.reshape(i, (50,100)))
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
                    #self.dump(x, i)

        return ms, time.time() - t, self.hash(img)

def risk(r, ev, ns, h):

    global prevra, ra
    global HR, HA

    p1 = (ra[0]-prevra[0]) * -1 if (ra[0]-prevra[0]) else 0
    p2 = ra[1]-prevra[1]

    #print("[R] %.5f %.5f [%d] %s" %(p1, p2, r, h))

    if p1 < 0:
        HR[h] = -1
    if p2 > 0:
        HR[h] = r

    def _act(r):
        if r == 0:
            for i in range(2):
                ryu.superpunch(i)
        elif r == 1:
            ryu.left()
            ryu.punch()
        elif r == 2:
            ryu.right()
            ryu.kick()
        elif r == 3:
            ryu.defendup(0)
            ryu.kick()
        elif r == 4:
            ryu.defendup(1)
            ryu.punch()
        elif r == 5:
            ryu.defenddown(0)
            ryu.downkick()
        elif r == 6:
            ryu.defenddown(1)
            ryu.downkick()
        elif r == 7:
            ryu.jumpleft()
            for i in range(2):
                ryu.fire(i)
        elif r == 8:
            ryu.jumpright()
            for i in range(2):
                ryu.superkick(i)
        elif r == 9:
            ryu.jumpup()
            ryu.kick()

    def _run(h, r):
        ns.value = True
        ev.set()

        if h in HR:
            z = HR[h]
            if z != -1:
                _act(z)
            else:
                _act(r)
        
        ns.value = False
        ev.set()

    z = False

    try:
        z = ns.value
        if not z:
            _run(h, r)

    except Exception, err:
        _run(h, r)
        pass

    ev.wait()

def advantage(a, ev, ns, h):

    global prevra, ra
    global HR, HA

    p1 = (ra[2]-prevra[2]) * -1 if (ra[2]-prevra[2]) else 0
    p2 = ra[3]-prevra[3]

    #print("[A] %.5f %.5f [%d] %s" %(p1, p2, a, h))

    if p1 < 0:
        HA[h] = -1
    if p2 > 0:
        HA[h] = a

    def _act(a):
        if a == 0:
            pass
        elif a == 1:
            ryu.punch()
        elif a == 2:
            ryu.kick()
        elif a == 3:
            ryu.downkick()
        elif a == 4:
            ryu.fire(0)
        elif a == 5:
            ryu.fire(1)
        elif a == 6:
            ryu.superpunch(0)
        elif a == 7:
            ryu.superpunch(1)
        elif a == 8:
            ryu.superkick(0)
        elif a == 9:
            ryu.superkick(1)

    def _run(h, a):
        ns.value = True
        ev.set()

        if h in HA:
            z = HA[h]
            if z != -1:
                _act(z)
            else:
                _act(a)

        ns.value = False
        ev.set()

    z = False

    try:
        z = ns.value
        if not z:
            _run(h, a)

    except Exception, err:
        _run(h, a)
        pass

    ev.wait()

def inference(x):

    global prevra, ra
    global HR, HA

    if len(PENALTY) > 0:
        msp, t, ip = image.minsubtract(PENALTY, x) 
        rp = numpy.random.choice(10, 1, p=[0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1])

    if len(REWARD) > 0:
        msr, t, ir = image.minsubtract(REWARD, x) 
        rr = numpy.random.choice(10, 1, p=[0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1])

    if msp < msr:
        ra[0], ra[1] = (0.4089536-sumb1/10000000.0), (0.4089536-sumb2/10000000.0)
        lenhr = 0.0
        for r in HR.values():
            if r != -1:
                lenhr += 1.0
        print("[R] %.5f (%.5f) %s [%d] (%.2f) [%.5f, %.5f]" %(msp, t, ip, rp, lenhr/float(len(PENALTY)), ra[0], ra[1]))
        r = multiprocessing.Process(target=risk, args=(rp, ev, ns, ip))
        r.start()
        #r.join()

    elif msp > msr: 
        ra[2], ra[3] = (0.4089536-sumb1/10000000.0), (0.4089536-sumb2/10000000.0)
        lenha = 0.0
        for a in HA.values(): 
            if a != -1:
                lenha += 1.0
        print("[A] %.5f (%.5f) %s [%d] (%.2f) [%.5f, %.5f]" %(msr, t, ir, rr, lenha/float(len(REWARD)), ra[2], ra[3]))
        a = multiprocessing.Process(target=advantage, args=(rr, ev, ns, ir))
        a.start()
        #a.join()

    prevra[0] = ra[0] 
    prevra[1] = ra[1] 
    prevra[2] = ra[2] 
    prevra[3] = ra[3] 

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

            elif sumb1 == BONUS[0] or sumb1 == BONUS[1] or sumb1 == BONUS[2] and not startGame:
                print '[Bonus]'

            elif sumb1 == BLOOD[0] and zsum == BLOOD[2]:
                print 'P1 [KO]'
                startGame = False
                time.sleep(1)

            elif sumb2 == BLOOD[0] and zsum == BLOOD[2]:
                print 'P2 [KO]'
                startGame = False
                pickle.dump(HR, open('pretrained/' + archive.enemy + '/' + 'HR-' + str(time.time()) + '.pkl', 'wb'))
                pickle.dump(HA, open('pretrained/' + archive.enemy + '/' + 'HA-' + str(time.time()) + '.pkl', 'wb'))
                time.sleep(1)

        elif sumb1 == RESUME[0]:
            ryu.insertcoin()
        
        elif sumb1 == RESUME[1]:
            ryu.select()
