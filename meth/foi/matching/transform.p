class Transform():

    def __init__(self):
        self.r = None
        self.g = None
        self.b = None
        self.gray = None

    def transform(self, frame, rgb):
        self.r = frame.copy()
        self.g = frame.copy()
        self.b = frame.copy()
        self.gray = frame.copy()

        if rgb == 'r':
            self.r[:,:,0] = 0
            self.r[:,:,1] = 0
            self.r[self.r < 250] = 0
            return self.r

        elif rgb == 'g':
            self.g[:,:,0] = 0
            self.g[:,:,2] = 0
            self.g[self.g < 250] = 0
            return self.g

        elif rgb == 'b':
            self.b[:,:,1] = 0
            self.b[:,:,2] = 0
            self.b[self.b < 250] = 0
            return self.b

        elif rgb == 'gray':
            self.gray[self.gray != 255] = 0
            g = cv2.cvtColor(self.gray, cv2.COLOR_BGR2GRAY)
            g[g > 127]
            return g
