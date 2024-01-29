#! /usr/bin/python3
# -*- coding: utf-8 -*-

import os
import sys
import cv2
import time
from glob import glob

# videos=sorted(glob("/home/hayashide/catkin_ws/src/sotsuron_experiment/results/20230605/movie/*"))
avi_path=sys.argv[1]

# for videoPath in videos:
cap=cv2.VideoCapture(avi_path)
ret,frame=cap.read()
fourcc = cv2.VideoWriter_fourcc('m','p','4', 'v')
print(frame)
size=(frame.shape[0],frame.shape[1])
video=cv2.VideoWriter(avi_path[:-4]+".mp4",fourcc, 30.0,size)
if cap.isOpened():
    while True:
        if ret:
            frame = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)
            video.write(frame)
            print("added a frame at:",time.time(),"frame shape:",(frame.shape[0],frame.shape[1]))
        else:
            break
        ret,frame=cap.read()
video.release()
del video
del cap
del fourcc