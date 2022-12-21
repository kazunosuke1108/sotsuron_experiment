from detectron2_core import *

import os
import numpy as np
import torch
import cv2
from glob import glob

"""
model type
OD: object detection
IS: instance segmentation
LVIS: LVinstance segmentation
PS: panoptic segmentation
KP: keypoint detection
"""

sources_path="/home/hayashide/catkin_ws/src/sotsuron_experiment/images/sources"
sources=sorted(glob(sources_path+"/*"))
print(sources)

results_path="/home/hayashide/catkin_ws/src/sotsuron_experiment/images/results"

for source in sources:
    pic_path=os.path.basename(source)
    detectron2_img=results_path+pic_path
    remap_img=results_path+"/remap/"+pic_path

    detector=Detector(model_type="KP")
    start=time.time()
    pred_keypoints=detector.onImage(source,detectron2_img)
    print(time.time()-start)

    try:
        np_pred_keypoints=pred_keypoints.to(torch.device('cpu')).detach().clone().numpy()[0]
    except IndexError:
        continue
    print(np_pred_keypoints)

    img=cv2.imread(source)

    for i,keypoint in enumerate(np_pred_keypoints):
        if float(keypoint[2])<0.4:
            paintCol=(0,0,255*(float(keypoint[2])+0.4))
            pass
        elif float(keypoint[2])<0.7:
            paintCol=(0,255*(float(keypoint[2])+0.7),0)
            pass
        else:
            paintCol=(255*(float(keypoint[2])),0,0)
            pass
        cv2.circle(img,
            center=(int(keypoint[0]), int(keypoint[1])),
            radius=10,
            color=paintCol,
            thickness=3,
            lineType=cv2.LINE_4,
            shift=0)
        cv2.putText(img,
                text=str(round(float(keypoint[2]),3)),
                org=(int(keypoint[0])+10, int(keypoint[1])),
                fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                fontScale=0.7,
                color=paintCol,
                thickness=2,
                lineType=cv2.LINE_4)
        cv2.putText(img,
                text=str(i),
                org=(int(keypoint[0])-30, int(keypoint[1])),
                fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                fontScale=0.7,
                color=paintCol,
                thickness=2,
                lineType=cv2.LINE_4)

    cv2.imwrite(remap_img,img)