import cv2

class TRANSFORM:

    def __init__(self):
        self.size = (400, 200)

    def blue(self, frame):
        b = frame.copy()
        b[:,:,1] = 0
        b[:,:,2] = 0
        b[b < 250] = 0
        return cv2.resize(b, self.size)

    def red(self, frame):
        r = frame.copy()
        r[:,:,0] = 0
        r[:,:,1] = 0
        r[r < 250] = 0
        return cv2.resize(r, self.size)

