#! /usr/bin/python3
# -*- coding: utf-8 -*-

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

videoPaths=["/home/hayashide/kazu_ws/sotsuron_experiment/sotsuron_experiment/results/_2023-12-11-11-55-46/_2023-12-11-11-55-46.mp4"]
skeletonVideoPaths=["/home/hayashide/kazu_ws/sotsuron_experiment/sotsuron_experiment/results/_2023-12-11-11-55-46/_2023-12-11-11-55-46_skeleton.mp4"]


for i, videoPath in enumerate(videoPaths):
    # videoPath="/home/hayashide/catkin_ws/src/sotsuron_experiment/results/20230526/movie/20230203_d_060_3_Yoshinari.mp4"

    cap=cv2.VideoCapture(videoPath)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    fourcc = cv2.VideoWriter_fourcc('m','p','4', 'v')
    writer = cv2.VideoWriter(skeletonVideoPaths[i],fourcc, fps, (width, height))
    detector=Detector(model_type="KP")


    while True:
        ret,frame=cap.read()
        if ret:
            cv2.imshow("source",frame)
            [pred_keypoints,output_img]=detector.onImage(image_mat=frame,return_skeleton=True)
            cv2.imshow("result",output_img)
            writer.write(output_img)

        key =cv2.waitKey(10)
        if key == 27:
            break

    writer.release()
    cap.release()
    cv2.destroyAllWindows()

# detector=Detector(model_type="KP")

# imgPath="/home/hayashide/catkin_ws/src/sotsuron_experiment/heavy/results/canvas_yolo.jpg"
# frame=cv2.imread(imgPath)
# [pred_keypoints,output_img]=detector.onImage(image_mat=frame,return_skeleton=True)
# cv2.imwrite("/home/hayashide/catkin_ws/src/sotsuron_experiment/heavy/results/canvas_yolo_kp.jpg",output_img)


# import os
# from glob import glob
# import subprocess as sp

# from detectron2_core import *
# """
# model type
# OD: object detection
# IS: instance segmentation
# LVIS: LVinstance segmentation
# PS: panoptic segmentation
# KP: keypoint detection
# """
# detector=Detector(model_type="KP")

# # results=detector.onImage(imagePath="/home/hayashide/catkin_ws/src/object_detector/images/sources/00_no_lost.jpeg")
# # print(list(detector.onImage(imagePath="/home/hayashide/catkin_ws/src/object_detector/images/sources/00_no_lost.jpeg")))#[0].numpy())
# # print(results)

# videos=sorted(glob("/home/hayashide/catkin_ws/src/sotsuron_experiment/results/20230526/movie/*"))
# print(videos)

# for videoPath in videos:
#     video_basename=os.path.basename(videoPath)
#     print(videoPath)
#     if video_basename[-4:]==".mp4":
#         detector.onVideo(videoPath=videoPath,savePath=f"/home/hayashide/catkin_ws//sotsuron_experiment/results/20230526/skeleton_movie/{video_basename}",csvPath=f'/home/hayashide/catkin_ws/src/object_detector/csv/{video_basename[:-4]}.csv')

# ######### 途中までやったなら、そこをスキップするのをお忘れなく！！！！！

# # #! /usr/bin/python3
# # # -*- coding: utf-8 -*-

# # import os
# # import sys
# # from glob import glob
# # import shutil
# # import json
# # import time
# # import datetime
# # import numpy as np

# # from detectron2_core import *

# # import os
# # import numpy as np
# # import torch
# # import cv2
# # from glob import glob

# # # videoPath="/home/hayashide/catkin_ws/src/sotsuron_experiment/results/0220/movie/20230220_d_090_30_shingo_ZED.mp4"
# # videoPath=sys.argv[1]
# # skeletonVideoPath=sys.argv[2]

# # cap=cv2.VideoCapture(videoPath)
# # width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
# # height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
# # fps = int(cap.get(cv2.CAP_PROP_FPS))
# # fourcc = cv2.VideoWriter_fourcc('m','p','4', 'v')
# # writer = cv2.VideoWriter(skeletonVideoPath,fourcc, fps, (width, height))
# # # Detectron2
# # detector=Detector(model_type="KP")
# # # YOLOv5
# # model = torch.hub.load("/usr/local/lib/python3.8/dist-packages/yolov5", 'custom', path=os.environ['HOME']+'/catkin_ws/src/object_detector/config/yolov5/yolov5s.pt',source='local')


# # while True:
# #     ret,frame=cap.read()
# #     if ret:
# #         cv2.imshow("source",frame)

# #         # Detectron2
# #         # [pred_keypoints,output_img]=detector.onImage(image_mat=frame,return_skeleton=True)
# #         # YOLOv5
# #         results=model(frame)
# #         objects=results.pandas().xyxy[0]
# #         obj_people=objects[objects['name']=='person']
# #         for i,row in enumerate(obj_people.itertuples()):
# #             # if row['confidence']<0.7:
# #             #     continue
# #             if row.confidence<0.7:
# #                 continue
# #             xmin=row.xmin
# #             ymin=row.ymin
# #             xmax=row.xmax
# #             ymax=row.ymax
# #             print(xmin)
# #             try:
# #                 cv2.rectangle(frame,pt1=(int(xmin),int(ymin)),pt2=(int(xmax),int(ymax)),color=(255,0,0),thickness=3)
# #             except cv2.error:
# #                 pass
# #         output_img=frame
        
# #         cv2.imshow("result",output_img)
# #         writer.write(output_img)

# #     key =cv2.waitKey(10)
# #     if key == 27:
# #         break

# # writer.release()
# # cap.release()
# # cv2.destroyAllWindows()

# # # detector=Detector(model_type="KP")

# # # imgPath="/home/hayashide/catkin_ws/src/sotsuron_experiment/heavy/results/canvas_yolo.jpg"
# # # frame=cv2.imread(imgPath)
# # # [pred_keypoints,output_img]=detector.onImage(image_mat=frame,return_skeleton=True)
# # # cv2.imwrite("/home/hayashide/catkin_ws/src/sotsuron_experiment/heavy/results/canvas_yolo_kp.jpg",output_img)