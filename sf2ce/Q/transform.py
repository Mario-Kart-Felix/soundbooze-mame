class TRANSFORM:

    def red(self, frame):
        r = frame.copy()
        r[:,:,0] = 0
        r[:,:,1] = 0
        r[r < 250] = 0
        return r

    def green(self, frame):
        g = frame.copy()
        g[:,:,0] = 0
        g[:,:,2] = 0
        g[g < 250] = 0
        return g

    def blue(self, frame):
        b = frame.copy()
        b[:,:,1] = 0
        b[:,:,2] = 0
        b[b < 250] = 0
        return b
