import cv2
import sys
import time
import numpy as np

from scipy.ndimage import uniform_filter

def crop(ar, crop_width):
    #from skimage.util import crop
    from numpy.lib.arraypad import _as_pairs
    crops = _as_pairs(crop_width, ar.ndim, as_index=True)
    slices = tuple(slice(a, ar.shape[i] - b) for i, (a, b) in enumerate(crops))
    cropped = ar[slices]
    return cropped

def ssim(X, Y):

    K1 = 0.01
    K2 = 0.03
    sigma = 1.5
    win_size = 7

    ndim = X.ndim

    X = np.array(X) * 1.0 #X = X.astype(np.float64)
    Y = np.array(Y) * 1.0 #Y = Y.astype(np.float64)

    NP = win_size ** ndim

    cov_norm = NP / (NP - 1)

    # pre simd
    ux = uniform_filter(X, win_size)
    uy = uniform_filter(Y, win_size)
    uxx = uniform_filter(X * X, win_size)
    uyy = uniform_filter(Y * Y, win_size)
    uxy = uniform_filter(X * Y, win_size)

    vx = cov_norm * (uxx - ux * ux)
    vy = cov_norm * (uyy - uy * uy)
    vxy = cov_norm * (uxy - ux * uy)

    R = 255
    C1 = (K1 * R) ** 2
    C2 = (K2 * R) ** 2

    A1, A2, B1, B2 = ((2 * ux * uy + C1,
                       2 * vxy + C2,
                       ux ** 2 + uy ** 2 + C1,
                       vx + vy + C2))
    D = B1 * B2
    S = (A1 * A2) / D

    pad = (win_size - 1) // 2

    mssim = crop(S, pad).mean()

    return mssim, S

img1 = cv2.imread(sys.argv[1], 0)
img2 = cv2.imread(sys.argv[2], 0)

ss, _ = ssim(img1, img2)
print ss
