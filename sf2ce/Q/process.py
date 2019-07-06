import numpy
import pickle
import Queue
import PIL
import imagehash

class PROCESS:

    def __init__(self, root):
        self.HQ = {}
        self.lr = .85
        self.y  = .99
        self.action = ['punch', 'kick', 'downkick', 'kick|right|kick', 'kick|jumpup|kick', 'jumpleft|kick', 'jumpright|kick', 'fire(0)', 'fire(1)', 'superpunch(0)', 'superpunch(1)', 'superkick(0)', 'superkick(1)', 'defendup(0)', 'defendup(1)', 'defenddown(0)', 'defenddown(1)'] 
        self.p = [1.0-(0.058*16), 0.058, 0.058, 0.058, 0.058, 0.058, 0.058, 0.058, 0.058, 0.058, 0.058, 0.058, 0.058, 0.058, 0.058, 0.058, 0.058]
        self.prevhit    = [0, 0]
        self.currenthit = [0, 0]
        self.que        = Queue.Queue()
        self.timeout    = 1.6
        self.root = root + '/'

    def _append(self, h):
        if not h in self.HQ:
            self.HQ[h] = [self.p, [0,0], numpy.zeros(len(self.p))]

    def _rminus(self, h, r):
        self.HQ[h][r] -= 0.01

    def _rplus(self, h, r):
        self.HQ[h][r] += 0.01

    def _hash(self, frame):
        return self._chop(imagehash.phash(frame))

    def _chop(self, h):
        hchop = ''
        hc = str(h)
        for i in range(len(hc)/2):
            hchop += hc[i]
        return hchop

    def _hitcount(self, sumb1, sumb2):
        self.currenthit[0], self.currenthit[1] = (0.4089536-sumb1/10000000.0), (0.4089536-sumb2/10000000.0)
        hit = [0, 0]
        hit[0], hit[1] = self.currenthit[0] - self.prevhit[0], self.currenthit[1] - self.prevhit[1]
        hit[0], hit[1] =  -1 if hit[0] else 0, 1 if hit[1] else 0
        return hit

    def _hitupdate(self):
        for i in range(2):
            self.prevhit[i] = self.currenthit[i]

    def act(self, curr):
        try:
            return numpy.argmax(self.HQ[curr][0]) + numpy.random.choice(len(self.p), 1, p=self.p)[0] #
        except:
            z = 1 - numpy.sum(self.p)
            if z != 0:
                return numpy.random.randint(0,16)
            else:
                return numpy.random.choice(len(self.p), 1, p=self.p)[0]

    def update(self, prev, a, curr, hit):
        try:
            self.HQ[prev][0][a] = self.HQ[prev][0][a] + self.lr * (numpy.sum(hit) + self.y * numpy.max(self.HQ[curr][0]) - self.HQ[prev][0][a])
        except:
            pass

    def process(self, prev, curr, player, sumb1, sumb2):

        r = None

        pink = PIL.Image.fromarray(prev)
        red = PIL.Image.fromarray(curr)
        hprev = self._hash(pink)
        hcurr = self._hash(red)

        self._append(hcurr)

        hit = self._hitcount(sumb1, sumb2)

        if hit[0] == 0 and hit[1] == 0:

            r = self.act(hcurr)
            player.act(r)
            hq = self.que.get(self.timeout)
            self.que.put((0))
            self.que.task_done()

            try:
                self.update(hprev, r, hcurr, hit)
                print("HQ[%d] - [%s] [%d %d] (%s)" %(len(self.HQ), hcurr, hit[0], hit[1], self.action[r]))
            except:
                pass

        self._hitupdate()

    def reduce(self):
       for k, v in self.HQ.items():
            if numpy.sum(self.HQ[k][1]) == 0:
                del self.HQ[k]

    def load(self, filename):
        self.HQ = pickle.load(open(filename, 'rb'))

    def save(self):
        self.reduce()
        pickle.dump(self.HQ, open(self.root + 'HQ.pkl', 'wb'))
