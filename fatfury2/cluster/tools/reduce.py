from skimage.measure import compare_ssim
import numpy
import time
import sys
import cv2
import os

input_path = sys.argv[1]

def similar(img_a, img_b):
    sim = 0.0
    try:
        img_a = cv2.resize(img_a, (200,100))
        img_b = cv2.resize(img_b, (200,100))
        sim, _ = compare_ssim(numpy.array(img_a), numpy.array(img_b), full=True, multichannel=True)
    except:
        pass
    return sim

for dir_path, subdir_list, file_list in os.walk(input_path):
    for fname in file_list:
        full_path = os.path.join(dir_path, fname)
        img1 = cv2.imread(full_path)

        for dp, sd_list, fl_list in os.walk(input_path):
            for fn in fl_list:
                fpath = os.path.join(dp, fn)
                img2 = cv2.imread(fpath)

                if full_path != fpath:
                    s = similar(img1, img2)
                    print s
                    if s > float(sys.argv[2]):  
                        print full_path, fpath
                        os.unlink(fpath)

'''
a = cv2.imread('tes/1561132784.03.png')
b = cv2.imread('tes/1561132784.05.png')
s = similar(a, b)
print s
'''

# python reduce.py dir/ 0.61
# python reduce.py dir/ 0.51
# python reduce.py dir/ 0.41
