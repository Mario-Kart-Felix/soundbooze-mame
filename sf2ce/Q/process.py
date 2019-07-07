import numpy
import pickle
import Queue
import PIL
import imagehash

class PROCESS:

    def __init__(self):
        self.HQ = {}
        self.lr = .85
        self.y  = .99
        self.action = ['punch', 'kick', 'downkick', 'kick|right|kick', 'kick|jumpup|kick', 'jumpleft|kick', 'jumpright|kick', 'fire(0)', 'fire(1)', 'superpunch(0)', 'superpunch(1)', 'superkick(0)', 'superkick(1)', 'defendup(0)', 'defendup(1)', 'defenddown(0)', 'defenddown(1)'] 
        self.p = [1.0-(0.058*16), 0.058, 0.058, 0.058, 0.058, 0.058, 0.058, 0.058, 0.058, 0.058, 0.058, 0.058, 0.058, 0.058, 0.058, 0.058, 0.058]
        self.que        = Queue.Queue()
        self.timeout    = 1.6
        self.wait       = True
        self.hash       = ['','', 0]

    def _append(self, h):
        if not h in self.HQ:
            self.HQ[h] = [self.p, [0,0], numpy.zeros(len(self.p))]

    def _hash(self, frame):
        return imagehash.phash(frame)

    def lock(self, p, n, r):
        self.hash[0], self.hash[1], self.hash[2] = p, n, r

    def rminus(self, h, r):
        try:
            self.HQ[h][2][r] -= 0.01
        except:
            pass

    def rplus(self, h, r):
        try:
            self.HQ[h][2][r] += 0.01
        except:
            pass

    def act(self, curr):
        try:
            return numpy.argmax(self.HQ[curr][0] + self.HQ[curr][2])
        except:
            return numpy.random.choice(len(self.p), 1, p=self.p)[0]

    def hit(self, h, hit):
        try:
            self.HQ[h][1] = hit
        except:
            pass

    def update(self, prev, a, curr, hit):
        try:
            self.HQ[prev][0][a] = self.HQ[prev][0][a] + self.lr * (numpy.sum(hit) + self.y * numpy.max(self.HQ[curr][0]) - self.HQ[prev][0][a])
        except:
            pass

    def process(self, prev, curr, player):

        def _log(hcurr, r):
            try:
                print("HQ[%d] - [%s]%s [%d %d] (%s)" %(len(self.HQ), hcurr, '*' if hcurr in self.HQ else '', self.HQ[hcurr][1][0], self.HQ[hcurr][1][1], self.action[r]))
            except:
                pass

        self.wait = True
        pink = PIL.Image.fromarray(prev)
        red = PIL.Image.fromarray(curr)
        hprev = self._hash(pink)
        hcurr = self._hash(red)
        self._append(hcurr)
        r = self.act(hcurr)
        player.act(r)
        self.lock(hprev, hcurr, r)
        self.wait = False
        
        _log(hcurr, r)
        _q, _ = self.que.get(self.timeout), self.que.task_done()

    def reduce(self):
        for k, v in self.HQ.items():
            if numpy.sum(v[1]) == 0:
                del self.HQ[k]

    def load(self, filename):
        self.HQ = pickle.load(open(filename, 'rb'))

    def save(self, root):
        self.reduce()
        pickle.dump(self.HQ, open(root + 'HQ.pkl', 'wb'))
