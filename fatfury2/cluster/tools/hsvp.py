import cv2
import numpy as np

white = np.uint8([[[255,255,255]]])
hsv_white = cv2.cvtColor(white,cv2.COLOR_BGR2HSV)
print hsv_white

red = np.uint8([[[0,0,255]]])
hsv_red = cv2.cvtColor(red,cv2.COLOR_BGR2HSV)
print hsv_red

yellow = np.uint8([[[0,255,255]]])
hsv_yellow = cv2.cvtColor(yellow,cv2.COLOR_BGR2HSV)
print hsv_yellow

green = np.uint8([[[0,255,0]]])
hsv_green = cv2.cvtColor(green,cv2.COLOR_BGR2HSV)
print hsv_green

aqua = np.uint8([[[255,255,0]]])
hsv_aqua = cv2.cvtColor(aqua,cv2.COLOR_BGR2HSV)
print hsv_aqua

blue = np.uint8([[[255,0,0]]])
hsv_blue = cv2.cvtColor(blue,cv2.COLOR_BGR2HSV)
print hsv_blue

#Now you take [H-10, 100,100] and [H+10, 255, 255] as lower bound and upper bound 
