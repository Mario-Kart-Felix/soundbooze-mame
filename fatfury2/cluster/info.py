import time
import socket
import hashlib 
import multiprocessing

class Info:

    def __init__(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        self.h = socket.gethostname()
        self.i = s.getsockname()[0]
        self.t = time.time()
        self.c = multiprocessing.cpu_count()
        s.close()

    def _hash(self, string):
        result = hashlib.md5(string)
        return result.hexdigest()

    def info(self):
        return self.h, self.i, self.t, self.c

    def constant(self):
        return self._hash(str(self.h)+str(self.i))

    def uniq(self):
        return self._hash(str(self.h)+str(i)+str(self.t)+str(self.c))

i = Info()

print 'INFO', i.info()
print 'CONSTANT', i.constant()
print 'UNIQ', i.uniq()
