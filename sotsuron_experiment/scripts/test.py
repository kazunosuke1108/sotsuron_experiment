import time
from detectron2_core import *
import cv2

img_path="000000000785.jpg"
for i in range(10):
    start=time.time()
    img=cv2.imread(img_path)
    detector=Detector(model_type="KP")
    pred_keypoints_t=detector.onImage(image_mat=img)
    print("######################################",time.time()-start)
