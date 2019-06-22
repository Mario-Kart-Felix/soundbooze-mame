'''
Lucas-Kanade homography tracker
===============================

Lucas-Kanade sparse optical flow demo. Uses goodFeaturesToTrack
for track initialization and back-tracking for match verification
between frames. Finds homography between reference and current views.

Usage
-----
lk_homography.py [<video_source>]
'''

import numpy as np
import cv2

lk_params = dict( winSize  = (19, 19), 
                  maxLevel = 2, 
                  criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))    

feature_params = dict( maxCorners = 1000, 
                       qualityLevel = 0.01,
                       minDistance = 8,
                       blockSize = 19 )

def checkedTrace(img0, img1, p0, back_threshold = 1.0):
    p1, st, err = cv2.calcOpticalFlowPyrLK(img0, img1, p0, None, **lk_params)
    p0r, st, err = cv2.calcOpticalFlowPyrLK(img1, img0, p1, None, **lk_params)
    d = abs(p0-p0r).reshape(-1, 2).max(-1)
    status = d < back_threshold
    return p1, status

blue = (5, 5, 5)
red = (0, 0, 255)

class App:
    def __init__(self, video_src):
        self.cam = cv2.VideoCapture(video_src)

    def run(self):

        while True:

            ret, frame = self.cam.read() #(406, 541, 3) 
            frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) # (406, 541)
            vis = frame.copy()

            frame0 = frame.copy()
            p0 = cv2.goodFeaturesToTrack(frame_gray, **feature_params)
            if p0 is not None:
                p1 = p0
                gray0 = frame_gray
                gray1 = frame_gray

            p2, trace_status = checkedTrace(gray1, frame_gray, p1)

            p1 = p2[trace_status].copy()
            p0 = p0[trace_status].copy()
            gray1 = frame_gray

            if len(p0) < 4:
                p0 = None
                continue
            
            H, status = cv2.findHomography(p0, p1, (0, cv2.RANSAC)[True], 10.0)
            h, w = frame.shape[:2]
            #overlay = cv2.warpPerspective(frame0, H, (w, h))
            #vis = cv2.addWeighted(vis, 0.5, overlay, 0.5, 0.0)
            
            for (x0, y0), (x1, y1), good in zip(p0[:,0], p1[:,0], status[:,0]):
                if good:
                    cv2.line(vis, (x0, y0), (x1, y1), (0, 128, 0))
                cv2.circle(vis, (x1, y1), 3, (red, blue)[good], -1)

            print('track count: %d' % len(p1))

            cv2.imshow('homography', vis)

            ch = 0xFF & cv2.waitKey(21)
            if ch == 27:
                break
                
def main():
    import sys
    try: video_src = sys.argv[1]
    except: video_src = 0

    print __doc__
    App(video_src).run()
    cv2.destroyAllWindows() 			

if __name__ == '__main__':
    main()
