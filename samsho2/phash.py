import PIL
import imagehash

class PHASH:

    def compute(self, frame):
        phash = str(imagehash.phash(PIL.Image.fromarray(frame)))
        return phash
