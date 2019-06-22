import os
import cv2
import mss

import time
import random
import numpy as np
import subprocess
import multiprocessing

import tensorflow as tf

from collections import deque
from keras.models import Sequential
from keras.layers import Dense
from keras.optimizers import Adam
from keras import backend as K

from scipy.stats import skew, kurtosis
from scipy.signal import find_peaks
from sklearn.cluster import KMeans

from PIL import Image
from PIL import ImageFilter

class RYU:

    def __init__(self, state_size, action_size):
        self.state_size = state_size
        self.action_size = action_size
        self.memory = deque(maxlen=5000)
        self.gamma = 0.95
        self.epsilon = 1.0
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.99
        self.learning_rate = 0.001
        self.model = self._build_model()
        self.target_model = self._build_model()
        self.update_target_model()

    def _huber_loss(self, y_true, y_pred, clip_delta=1.0):
        error = y_true - y_pred
        cond  = K.abs(error) <= clip_delta
        squared_loss = 0.5 * K.square(error)
        quadratic_loss = 0.5 * K.square(clip_delta) + clip_delta * (K.abs(error) - clip_delta)
        return K.mean(tf.where(cond, squared_loss, quadratic_loss))

    def _build_model(self):
        model = Sequential()
        model.add(Dense(24, input_dim=self.state_size, activation='relu'))
        model.add(Dense(24, activation='relu'))
        model.add(Dense(self.action_size, activation='linear'))
        model.compile(loss=self._huber_loss, optimizer=Adam(lr=self.learning_rate))
        return model

    def update_target_model(self):
        self.target_model.set_weights(self.model.get_weights())

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def act(self, state):
        if np.random.rand() <= self.epsilon:
            return random.randrange(self.action_size)
        act_values = self.model.predict(state)
        return np.argmax(act_values[0])

    def replay(self, batch_size):
        minibatch = random.sample(self.memory, batch_size)
        for state, action, reward, next_state, done in minibatch:
            target = self.model.predict(state)
            if done:
                target[0][action] = reward
            else:
                t = self.target_model.predict(next_state)[0]
                target[0][action] = reward + self.gamma * np.amax(t)
            self.model.fit(state, target, epochs=1, verbose=0)
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

    def load(self, name):
        self.model.load_weights(name)

    def save(self, name):
        self.model.save_weights(name)

    def reward_penalty(self, img, prevBlood):
        b = img[:, :, 0]
        g = img[:, :, 1]
        ssum = np.sum(b.ravel()) + np.sum(g.ravel())
        current = ((float(ssum)))
        sub = np.sqrt(prevBlood - current)/1000.0
        if current != prevBlood:
            return sub, current
        else:
            return 0, 0

    def focus(self, winid):
        os.system('xdotool windowfocus --sync ' + winid)

    def kick(self, winid):
        for i in range(0,2):
            os.system('xdotool key --window ' + winid + ' key C')

    def defendup(self, winid, pos):
        key = "Left"
        if pos == 0:
            key = "Left"
        elif pos == 1:
            key = "Right"

        os.system('xdotool key --window ' + winid + ' keydown ' + key)
        time.sleep(0.6)
        os.system('xdotool key --window ' + winid + ' keyup ' + key)

    def defenddown(self, winid, pos):
        key = "Left"
        if pos == 0:
            key = "Left"
        elif pos == 1:
            key = "Right"

        os.system('xdotool key --window ' + winid + ' keydown ' + key)
        os.system('xdotool key --window ' + winid + ' keydown Down')
        time.sleep(0.6)
        os.system('xdotool key --window ' + winid + ' keyup ' + key)
        os.system('xdotool key --window ' + winid + ' keyup Down')

    def downkick(self, winid):
        os.system('xdotool key --window ' + winid + ' keydown Down')
        for i in range(0,2):
            os.system('xdotool key --window ' + winid + ' key C')
        os.system('xdotool key --window ' + winid + ' keyup Down')

    def punch(self, winid):
        for i in range(0,2):
            os.system('xdotool key --window ' + winid + ' key D')

    def left(self, winid):
        os.system('xdotool key --window ' + winid + ' keydown Left')
        time.sleep(0.9)
        os.system('xdotool key --window ' + winid + ' keyup Left')

    def right(self, winid):
        os.system('xdotool key --window ' + winid + ' keydown Right')
        time.sleep(0.9)
        os.system('xdotool key --window ' + winid + ' keyup Right')

    def jumpright(self, winid):
        os.system('xdotool key --window ' + winid + ' keydown Right')
        os.system('xdotool key --window ' + winid + ' keydown Up')
        time.sleep(0.5)
        os.system('xdotool key --window ' + winid + ' keyup Right')
        os.system('xdotool key --window ' + winid + ' keyup Up')

    def jumpleft(self, winid):
        os.system('xdotool key --window ' + winid + ' keydown Left')
        os.system('xdotool key --window ' + winid + ' keydown Up')
        time.sleep(0.5)
        os.system('xdotool key --window ' + winid + ' keyup Left')
        os.system('xdotool key --window ' + winid + ' keyup Up')

    def jumpup(self, winid):
        os.system('xdotool key --window ' + winid + ' key Up')

    def fire(self, winid, pos):
        z = "Right"
        if pos == 0:
            z = "Right"
        else:
            z = "Left"

        os.system('xdotool key --window ' + winid + ' keydown Down')
        os.system('xdotool key --window ' + winid + ' keydown ' + z)
        os.system('xdotool key --window ' + winid + ' keyup Down')
        os.system('xdotool key --window ' + winid + ' keydown D')
        os.system('xdotool key --window ' + winid + ' keyup ' + z)
        os.system('xdotool key --window ' + winid + ' keyup D')

    def superkick(self, winid, pos):
        z = "Left"
        if pos == 0:
            z = "Left"
        else:
            z = "Right"

        os.system('xdotool key --window ' + winid + ' keydown Down')
        os.system('xdotool key --window ' + winid + ' keydown ' + z)
        os.system('xdotool key --window ' + winid + ' keyup Down')
        os.system('xdotool key --window ' + winid + ' keydown C')
        os.system('xdotool key --window ' + winid + ' keyup ' + z)
        os.system('xdotool key --window ' + winid + ' keyup C')

    def superpunch(self, winid, pos):
        z = "Right"
        if pos == 0:
            z = "Right"
        else:
            z = "Left"

        os.system('xdotool key --window ' + winid + ' keydown ' + z)
        os.system('xdotool key --window ' + winid + ' keydown Down')

        os.system('xdotool key --window ' + winid + ' keyup ' + z)
        os.system('xdotool key --window ' + winid + ' keyup Down')

        os.system('xdotool key --window ' + winid + ' keydown Down')
        os.system('xdotool key --window ' + winid + ' keydown ' + z)

        os.system('xdotool key --window ' + winid + ' keyup Down')
        os.system('xdotool key --window ' + winid + ' keydown D')
        os.system('xdotool key --window ' + winid + ' keyup ' + z)
        os.system('xdotool key --window ' + winid + ' keyup D')

if __name__ == "__main__":
    
    state_size = 8 * 2
    action_size = 4
    batch_size = 32
    ryu = RYU(state_size, action_size)

    #training on the go - per 1 round fight (pen/rew snap)
    #ambigu-state, reward-bias, jarak...
    #defense reward (jump-fireball(left/r),kick,/etc)  #reward 0, <
    #ryu.load("sf2.h5")
    #ryu.save("sf2.h5")

    def _similar(img_a, img_b):
        from skimage.measure import compare_ssim
        i = cv2.cvtColor(cv2.resize(img_a, (200, 150)), cv2.COLOR_BGR2GRAY)
        j = cv2.cvtColor(cv2.resize(img_b, (200, 150)), cv2.COLOR_BGR2GRAY)
        sim, _ = compare_ssim(i, j, full=True)
        return sim

    def _calc_histogram(img):
        num = np.prod(img.shape[:2])
        hist = cv2.calcHist([img], [0], None, [16], [0, 255]) / num
        s = skew(hist)
        k = kurtosis(hist)
        v = np.var(hist)
        hsum = np.sum(hist)/100.0
        m = (s + k + v + hsum) / 4
        return m 

    def _crop(img, l, t, width, height):
        im_pil = Image.fromarray(img)
        im_crop = im_pil.crop((l, t, l+width, t+height))
        z = np.asarray(im_crop)
        return z

    def _edgesum(img, l, t, width, height):
        mask = subtractor.apply(_crop(img, l, t, width, height))
        blur = cv2.GaussianBlur(mask,(5,5),0)
        pil_img = Image.fromarray(blur)
        edge = np.array(pil_img.filter(ImageFilter.FIND_EDGES))
        edgecv = cv2.cvtColor(np.array(edge), cv2.COLOR_RGB2BGR)
        blursum = (np.sum(blur)/1000000.0)
        return _calc_histogram(blur), blursum, blur

    def _collect(img):
        head_m, head_blursum, head_img = _edgesum(img, 0, 310, 800, 100)
        leg_m, leg_blursum, leg_img = _edgesum(img, 0, 470, 800, 100)

        HEAD = []
        if head_m > 0:
            if head_blursum > 0.0:# and head_blursum < 3.8: [TUNE]
                H = np.hsplit(head_img, 8)
                for h in H:
                    sk = np.sum(h)/1000000.0
                    if sk < 0.9: #[TUNE]
                        HEAD.append(sk) # HEAD.append(1) #[TUNE] 
                    else:
                        HEAD.append(0)

        LEG = []
        if leg_m > 0:
            if leg_blursum > 0.0:# and leg_blursum < 3.8: [TUNE]
                H = np.hsplit(leg_img, 8)
                for h in H:
                    sk = np.sum(h)/1000000.0
                    if sk < 0.9: #[TUNE]
                        LEG.append(sk) # LEG.append(1) #[TUNE]
                    else:
                        LEG.append(0)

        #print head_blursum, leg_blursum
        return HEAD, LEG

    def _winid():
        cmd = "xdotool search --pid `pgrep mame`"
        r =  subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE).stdout
        v = r.read()
        return hex(int(v.decode()))

    with mss.mss() as sct:

        winid = _winid()
        ryu.focus(winid)

        border = 24
        monitor = {"top": 100+border, "left": 100, "width": 800, "height":600-border}
        subtractor = cv2.createBackgroundSubtractorMOG2(history=20, varThreshold=25, detectShadows=True)

        prevBloodP1 = 0
        prevBloodP2 = 0

        startGame = False

        HH = []
        state = np.reshape(np.zeros(state_size), [1, state_size])
        reward = 0.0
        R = 0.0

        NS = []

        prev_p1 = np.array(sct.grab(monitor))

        while [ 1 ]:

            p1 = np.array(sct.grab(monitor))
            p2 = p1.copy()

            b1 = p1[60:78, 68:364]
            b2 = p2[60:78, 68+366:364+366]
    
            sp1, curp1 = ryu.reward_penalty(b1, prevBloodP1)
            sp2, curp2 = ryu.reward_penalty(b2, prevBloodP2)

            sumb1 = np.sum(b1)
            sumb2 = np.sum(b2)

            scs = _similar(prev_p1, p1)
            #print '[Scene]', scs
            prev_p1 = p1

            if sumb1 >= 2744512 and sumb1 <= 4089536: # [Round]

                if sumb1 == 4089536 and sumb2 == 4089536 and not startGame:
                    print '[Start]'
                    reward = 0.0
                    R = 0.0
                    startGame = True
                    time.sleep(2)

                if sumb1 == 2744512:
                    print 'P1 [KO]' #err
                    startGame = False
                    reward = reward - 100.0
                    #time.sleep(5)

                elif sumb2 == 2744512:
                    print 'P2 [KO]' #err
                    startGame = False
                    reward = reward + 100.0
                    #ryu.update_target_model()
                    #time.sleep(5)

                if (sp1 != 0 and sp2 != 0):
                    if np.isnan(sp1):
                        sp1=0
                    if np.isnan(sp2):
                        sp2=0

                    if sp1 > 0:
                        reward = reward - 5.0
                    elif sp2 > 0:
                        reward = reward + 5.0
                    else:
                        reward = 0.0

                HEAD, LEG = _collect(p1)

                # [TUNE], idle [] && < 4, sync HEAD/LEG, posisi kanan err..., state/nextstate
                if len(HEAD) > 0 and len(LEG) > 0:
                    
                    HH.append(HEAD)
                    HH.append(LEG)
                    
                    #print np.matrix(HH)
                    #print ''

                    if len(NS) < batch_size/4:
                        h = skew(HH[0])
                        l = skew(HH[1])
                        NS.append([h, l, scs])
                    else:
                        k = KMeans(n_clusters=2, n_jobs=-1, random_state=128)
                        k.fit(NS)
                        NS = []
                        z = np.array([skew(HH[0]),skew(HH[1]), scs])
                        p = k.predict([z])
                        print '[Cluster]', p[0]
                        if p[0] == 0:
                            ryu.jumpleft(winid)
                            ryu.kick(winid)
                        elif p[0] == 1:
                            ryu.jumpright(winid)
                            ryu.kick(winid)

                    state = np.reshape(HH, [1, state_size])
                    action = ryu.act(state)

                    # [TUNE] - pred.posisi non-templateMatch L/R , defend/attack LogReg
                    if action == 0:
                        ryu.fire(winid, 0)

                    elif action == 1:
                        ryu.superkick(winid, 0)

                    elif action == 2:
                        ryu.superpunch(winid, 0)

                    elif action == 3:
                        ryu.kick(winid)
                        ryu.punch(winid)

                    next_state = np.reshape(HH, [1, state_size])

                    ryu.remember(state, action, reward, next_state, startGame) # [TUNE] - metrics p5
                    state = next_state

                    if len(ryu.memory) > batch_size:
                        ryu.replay(batch_size)

                    HH = []

                    R = R + reward 
                    print '[Action]', action, '[Reward]', reward, '[Rewards]', R

                prevBloodP1 = curp1
                prevBloodP2 = curp2

            elif sumb1 == 1358640:  
                os.system('xdotool key --window ' + winid + ' keydown 5')
                time.sleep(0.2)
                os.system('xdotool key --window ' + winid + ' keyup 5')
                time.sleep(0.2)
                os.system('xdotool key --window ' + winid + ' key 1')
            elif sumb1 == 2623509:
                time.sleep(1)
                os.system('xdotool key --window ' + winid + ' key A')
                time.sleep(2)
