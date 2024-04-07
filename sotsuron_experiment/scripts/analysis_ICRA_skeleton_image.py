#! /usr/bin/python3
# -*- coding: utf-8 -*-

from detectron2_core import *

import os
import numpy as np
import torch
import cv2
from glob import glob

image_path="/home/hayashide/catkin_ws/src/sotsuron_experiment/analysis/icra/画像2.png"
results_image_path=image_path[:-4]+"_skeleton.png"
detector=Detector(model_type="KP")
pred_keypoints=detector.onImage(imagePath=image_path,savePath=results_image_path)