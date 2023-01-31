#! /usr/bin/python3
# -*- coding: utf-8 -*-

import os
import sys
from glob import glob
import shutil
import json
import time
import datetime
import numpy as np

from detectron2_core import *

import os
import numpy as np
import torch
import cv2
from glob import glob

videoPath="/home/hayashide/catkin_ws/src/sotsuron_experiment/heavy/20230117_d_060_1_Hayashide.mp4"

# cap=cv2.VideoCapture(videoPath)
# width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
# height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
# fps = int(cap.get(cv2.CAP_PROP_FPS))
# fourcc = cv2.VideoWriter_fourcc('m','p','4', 'v')
# writer = cv2.VideoWriter("/home/hayashide/catkin_ws/src/sotsuron_experiment/heavy/results/skeleton.mp4",fourcc, fps, (width, height))
# detector=Detector(model_type="KP")


# while True:
#     ret,frame=cap.read()
#     if ret:
#         cv2.imshow("source",frame)
#         [pred_keypoints,output_img]=detector.onImage(image_mat=frame,return_skeleton=True)
#         cv2.imshow("result",output_img)
#         writer.write(output_img)

#     key =cv2.waitKey(10)
#     if key == 27:
#         break

# writer.release()
# cap.release()
# cv2.destroyAllWindows()

detector=Detector(model_type="KP")

imgPath="/home/hayashide/catkin_ws/src/sotsuron_experiment/heavy/results/canvas_yolo.jpg"
frame=cv2.imread(imgPath)
[pred_keypoints,output_img]=detector.onImage(image_mat=frame,return_skeleton=True)
cv2.imwrite("/home/hayashide/catkin_ws/src/sotsuron_experiment/heavy/results/canvas_yolo_kp.jpg",output_img)