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

sources_path="/home/hayashide/catkin_ws/src/sotsuron_experiment/analysis/icra"
sources=sorted(glob(sources_path+"/*.png"))
print(sources)

results_path="/home/hayashide/catkin_ws/src/sotsuron_experiment/analysis/icra"

for source in sources:
    pic_path=os.path.basename(source)
    detectron2_img=results_path+pic_path
    remap_img=results_path+"/remap/"+pic_path

    detector=Detector(model_type="KP")
    start=time.time()
    pred_keypoints=detector.onImage(source,detectron2_img)
    print(time.time()-start)

    try:
        img=cv2.imread(source)
        for idx in range(len(pred_keypoints.to(torch.device('cpu')).detach().clone().numpy())):
            print(idx)
            np_pred_keypoints=pred_keypoints.to(torch.device('cpu')).detach().clone().numpy()[idx]
            print(np_pred_keypoints)


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
            paintCol=(255,0,0)
            # 頭部
            cv2.line(img,
                     pt1=(int(np_pred_keypoints[0,0]),int(np_pred_keypoints[0,1])),
                     pt2=(int(np_pred_keypoints[1,0]),int(np_pred_keypoints[1,1])),
                     color=paintCol,
                     thickness=3,
                     )
            cv2.line(img,
                     pt1=(int(np_pred_keypoints[1,0]),int(np_pred_keypoints[1,1])),
                     pt2=(int(np_pred_keypoints[3,0]),int(np_pred_keypoints[3,1])),
                     color=paintCol,
                     thickness=3,
                     )
            cv2.line(img,
                     pt1=(int(np_pred_keypoints[0,0]),int(np_pred_keypoints[0,1])),
                     pt2=(int(np_pred_keypoints[2,0]),int(np_pred_keypoints[2,1])),
                     color=paintCol,
                     thickness=3,
                     )
            cv2.line(img,
                     pt1=(int(np_pred_keypoints[2,0]),int(np_pred_keypoints[2,1])),
                     pt2=(int(np_pred_keypoints[4,0]),int(np_pred_keypoints[4,1])),
                     color=paintCol,
                     thickness=3,
                     )
            # 体幹
            paintCol=(0,255,0)
            cv2.line(img,
                     pt1=(int(np_pred_keypoints[0,0]),int(np_pred_keypoints[0,1])),
                     pt2=(int((np_pred_keypoints[11,0]+np_pred_keypoints[12,0])/2),int((np_pred_keypoints[11,1]+np_pred_keypoints[12,1])/2)),
                     color=paintCol,
                     thickness=3,
                     )
            cv2.line(img,
                     pt1=(int(np_pred_keypoints[5,0]),int(np_pred_keypoints[5,1])),
                     pt2=(int(np_pred_keypoints[6,0]),int(np_pred_keypoints[6,1])),
                     color=paintCol,
                     thickness=3,
                     )
            cv2.line(img,
                     pt1=(int(np_pred_keypoints[11,0]),int(np_pred_keypoints[11,1])),
                     pt2=(int(np_pred_keypoints[12,0]),int(np_pred_keypoints[12,1])),
                     color=paintCol,
                     thickness=3,
                     )
            # 2の腕
            cv2.line(img,
                     pt1=(int(np_pred_keypoints[5,0]),int(np_pred_keypoints[5,1])),
                     pt2=(int(np_pred_keypoints[7,0]),int(np_pred_keypoints[7,1])),
                     color=paintCol,
                     thickness=3,
                     )
            cv2.line(img,
                     pt1=(int(np_pred_keypoints[6,0]),int(np_pred_keypoints[6,1])),
                     pt2=(int(np_pred_keypoints[8,0]),int(np_pred_keypoints[8,1])),
                     color=paintCol,
                     thickness=3,
                     )
            # 手先
            cv2.line(img,
                     pt1=(int(np_pred_keypoints[7,0]),int(np_pred_keypoints[7,1])),
                     pt2=(int(np_pred_keypoints[9,0]),int(np_pred_keypoints[9,1])),
                     color=paintCol,
                     thickness=3,
                     )
            cv2.line(img,
                     pt1=(int(np_pred_keypoints[8,0]),int(np_pred_keypoints[8,1])),
                     pt2=(int(np_pred_keypoints[10,0]),int(np_pred_keypoints[10,1])),
                     color=paintCol,
                     thickness=3,
                     )
            paintCol=(0,0,255)
            # 膝
            cv2.line(img,
                     pt1=(int(np_pred_keypoints[11,0]),int(np_pred_keypoints[11,1])),
                     pt2=(int(np_pred_keypoints[13,0]),int(np_pred_keypoints[13,1])),
                     color=paintCol,
                     thickness=3,
                     )
            cv2.line(img,
                     pt1=(int(np_pred_keypoints[12,0]),int(np_pred_keypoints[12,1])),
                     pt2=(int(np_pred_keypoints[14,0]),int(np_pred_keypoints[14,1])),
                     color=paintCol,
                     thickness=3,
                     )
            # 足先
            cv2.line(img,
                     pt1=(int(np_pred_keypoints[13,0]),int(np_pred_keypoints[13,1])),
                     pt2=(int(np_pred_keypoints[15,0]),int(np_pred_keypoints[15,1])),
                     color=paintCol,
                     thickness=3,
                     )
            cv2.line(img,
                     pt1=(int(np_pred_keypoints[14,0]),int(np_pred_keypoints[14,1])),
                     pt2=(int(np_pred_keypoints[16,0]),int(np_pred_keypoints[16,1])),
                     color=paintCol,
                     thickness=3,
                     )
            
            
            
                # cv2.putText(img,
                #         text=str(round(float(keypoint[2]),3)),
                #         org=(int(keypoint[0])+10, int(keypoint[1])),
                #         fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                #         fontScale=0.7,
                #         color=paintCol,
                #         thickness=2,
                #         lineType=cv2.LINE_4)
                # cv2.putText(img,
                #         text=str(i),
                #         org=(int(keypoint[0])-30, int(keypoint[1])),
                #         fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                #         fontScale=0.7,
                #         color=paintCol,
                #         thickness=2,
                #         lineType=cv2.LINE_4)

    except IndexError:
        continue
    cv2.imwrite(remap_img,img)