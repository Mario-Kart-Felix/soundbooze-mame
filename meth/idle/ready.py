# -*- coding: utf-8 -*-

import os
import cv2
import mss
import time
import numpy

import matplotlib.pyplot as plt
from scipy.signal import find_peaks
from skimage.measure import compare_ssim

SPLIT        =    2
TOTAL_SAMPLE =  200

def similar(img_a, img_b):
    img_a = cv2.cvtColor(img_a, cv2.COLOR_BGR2GRAY)
    img_b = cv2.cvtColor(img_b, cv2.COLOR_BGR2GRAY)
    h, w = img_a.shape
    img_a = cv2.resize(img_a, (w/SPLIT/2, h/SPLIT/2))
    img_b = cv2.resize(img_b, (w/SPLIT/2, h/SPLIT/2))
    sim, _ = compare_ssim(numpy.array(img_a), numpy.array(img_b), full=True)
    return sim

with mss.mss() as sct:

    body = {"top": 284, "left": 100, "width": 800, "height": 300+24}

    frames_r, frames_g, frames_b = [], [], []
    prevframes_r, prevframes_g, prevframes_b = [], [], []

    frame_b = numpy.array(sct.grab(body))

    red, green, blue = frame_b.copy(), frame_b.copy(), frame_b.copy()

    # body

    red[:,:,0] = 0
    red[:,:,1] = 0
    red[red < 250] = 0

    green[:,:,0] = 0
    green[:,:,2] = 0
    green[green < 250] = 0

    blue[:,:,1] = 0
    blue[:,:,2] = 0
    blue[blue < 250] = 0

    prevframes_r.append(red)
    prevframes_g.append(green)
    prevframes_b.append(blue)

    R, G, B = [], [], []
    i = 0

    directory = str(time.time()) + '/'
    os.mkdir(directory)

    while [ 1 ]:

        frame_b = numpy.array(sct.grab(body))
        cv2.imwrite(directory + str(i) + '.png', frame_b)

        red, green, blue = frame_b.copy(), frame_b.copy(), frame_b.copy()

        # body

        red[:,:,0] = 0
        red[:,:,1] = 0
        red[red < 250] = 0

        green[:,:,0] = 0
        green[:,:,2] = 0
        green[green < 250] = 0

        blue[:,:,1] = 0
        blue[:,:,2] = 0
        blue[blue < 250] = 0

        frames_r.append(red)
        frames_g.append(green)
        frames_b.append(blue)

        for pr, fr in zip(prevframes_r, frames_r):
            s = similar(pr, fr)
            R.append(1-s)

        for pg, fg in zip(prevframes_g, frames_g):
            s = similar(pg, fg)
            G.append(1-s)

        for pb, fb in zip(prevframes_b, frames_b):
            s = similar(pb, fb)
            B.append(1-s)

        # prev = current

        frames_r, frames_g, frames_b = [], [], []
        prevframes_r, prevframes_g, prevframes_b = [], [], []

        red, green, blue = frame_b.copy(), frame_b.copy(), frame_b.copy()

        # body

        red[:,:,0] = 0
        red[:,:,1] = 0
        red[red < 250] = 0

        green[:,:,0] = 0
        green[:,:,2] = 0
        green[green < 250] = 0

        blue[:,:,1] = 0
        blue[:,:,2] = 0
        blue[blue < 250] = 0

        prevframes_r.append(red)
        prevframes_g.append(green)
        prevframes_b.append(blue)

        if i != 0 and i % TOTAL_SAMPLE == 0:

            plt.subplot(511)
            plt.plot(R, color='red')
            plt.subplot(512)
            plt.plot(G, color='green')
            plt.subplot(513)
            plt.plot(B, color='blue')
            plt.subplot(514)

            idr = numpy.argmax(R)
            idg = numpy.argmax(G)
            idb = numpy.argmax(B)

            print idr, R[idr]
            print idg, G[idg]
            print idb, B[idb]

            Z = [numpy.sum(R), numpy.sum(G), numpy.sum(B)]
            ic = numpy.argmin(Z)
            C = numpy.array([R, G, B])

            peaks, _ = numpy.array(find_peaks(C[ic]))
            cpx = C[ic][peaks]
            plt.plot(C[ic])
            plt.plot(peaks, cpx, "x")

            plt.subplot(515)
            found = cv2.imread(directory + str(idr) + '.png')
            plt.imshow(numpy.array(found))
            plt.show()

            os.system('rm -rf ' + directory)

            R, G, B= [], [], []

            break

        i += 1
