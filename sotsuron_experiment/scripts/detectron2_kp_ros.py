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
import cv2
import rospy
import tf
import torch
from pprint import pprint
from sensor_msgs.msg import Image
from sensor_msgs.msg import CameraInfo
import message_filters
from cv_bridge import CvBridge

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

rospy.init_node('detectron2_subscriber')
csv_path=os.environ['HOME']+"/catkin_ws/src/sotsuron_experiment/gaits/gaits_stop_10.csv"

gravity_history=[]

def pub_sub():
    global rgb_sub,dpt_sub,info_sub
    # subscriber
    sub_list=[]
    rgb_sub=message_filters.Subscriber(topicName_rgb,Image)
    sub_list.append(rgb_sub)
    dpt_sub=message_filters.Subscriber(topicName_dpt,Image)
    sub_list.append(dpt_sub)
    info_sub=message_filters.Subscriber(topicName_camInfo,CameraInfo)
    sub_list.append(info_sub)
    mf=message_filters.ApproximateTimeSynchronizer(sub_list,10,0.5)
    
    # publisher

    # listener

    # broadcaster

    return mf

def detect_kp(rgb_array):
    # rospy.loginfo("####### debug ROI #######")
    pred_keypoints=detector.onImage(image_mat=rgb_array)
    np_pred_keypoints=pred_keypoints.to(torch.device('cpu')).detach().clone().numpy()[0]
    return np_pred_keypoints

def get_position_kp(rgb_array,dpt_array,np_pred_keypoints,proj_mtx):
    # size translation
    y_rgb2dpt=dpt_array.shape[0]/rgb_array.shape[0]
    x_rgb2dpt=dpt_array.shape[1]/rgb_array.shape[1]

    pred_keypoints_3D=[]

    for i, kp in enumerate(np_pred_keypoints):
        kp_0=kp[0]*y_rgb2dpt
        kp_1=kp[1]*x_rgb2dpt
        size_bdbox=30
        dpt=np.nanmedian(dpt_array[int(kp_1)-size_bdbox:int(kp_1)+size_bdbox,int(kp_0)-size_bdbox:int(kp_0)+size_bdbox])
        # rospy.loginfo(f"{kp_0},{kp_1},{dpt}")
        # rospy.loginfo(dpt_array[int(kp_0)-size_bdbox:int(kp_0)+size_bdbox,int(kp_1)-size_bdbox:int(kp_1)+size_bdbox])
        kp_3d=dpt*np.dot(np.linalg.pinv(proj_mtx),np.array([kp_0,kp_1,1]).T)
        # rospy.loginfo(dpt)
        pred_keypoints_3D.append(kp_3d.tolist())
    np_pred_keypoints_3D=np.array(pred_keypoints_3D)
    return np_pred_keypoints_3D

def get_gravity_zone(np_pred_keypoints_3D):
    mass={
        "head":0.044,
        "neck":0.033,
        "body":0.479,
        "upper_arm":0.0265,
        "lower_arm":0.015,
        "hand":0.009,
        "upper_leg":0.1,
        "lower_leg":0.0535,
        "foot":0.019
    }
    total_mass=mass["head"]+mass["neck"]+mass["body"]+2*(mass["upper_arm"]+mass["lower_arm"]+mass["hand"]+mass["upper_leg"]+mass["lower_leg"]+mass["foot"])
    position={
        "head":1/5*(np_pred_keypoints_3D[0]+np_pred_keypoints_3D[1]+np_pred_keypoints_3D[2]+np_pred_keypoints_3D[3]+np_pred_keypoints_3D[4]),
        "neck":1/3*(np_pred_keypoints_3D[0]+np_pred_keypoints_3D[1]+np_pred_keypoints_3D[2]),
        "body":1/4*(np_pred_keypoints_3D[5]+np_pred_keypoints_3D[6]+np_pred_keypoints_3D[11]+np_pred_keypoints_3D[12]),
        "upper_arm_L":1/2*(np_pred_keypoints_3D[5]+np_pred_keypoints_3D[7]),
        "upper_arm_R":1/2*(np_pred_keypoints_3D[6]+np_pred_keypoints_3D[8]),
        "lower_arm_L":1/2*(np_pred_keypoints_3D[7]+np_pred_keypoints_3D[9]),
        "lower_arm_R":1/2*(np_pred_keypoints_3D[8]+np_pred_keypoints_3D[10]),
        "hand_L":np_pred_keypoints_3D[9],
        "hand_R":np_pred_keypoints_3D[10],
        "upper_leg_L":1/2*(np_pred_keypoints_3D[11]+np_pred_keypoints_3D[13]),
        "upper_leg_R":1/2*(np_pred_keypoints_3D[12]+np_pred_keypoints_3D[14]),
        "lower_leg_L":1/2*(np_pred_keypoints_3D[13]+np_pred_keypoints_3D[15]),
        "lower_leg_R":1/2*(np_pred_keypoints_3D[14]+np_pred_keypoints_3D[16]),
        "foot_L":np_pred_keypoints_3D[15],
        "foot_R":np_pred_keypoints_3D[16]
    }
    part_gravity={
        "head":mass['head']*position['head'],
        "neck":mass['neck']*position['neck'],
        "body":mass['body']*position['body'],
        "upper_arm":mass['upper_arm']*(position['upper_arm_L']+position['upper_arm_R']),
        "lower_arm":mass['lower_arm']*(position['lower_arm_L']+position['lower_arm_R']),
        "hand":mass['hand']*(position['hand_L']+position['hand_R']),
        "upper_leg":mass['upper_leg']*(position['upper_leg_L']+position['upper_leg_R']),
        "lower_leg":mass['lower_leg']*(position['lower_leg_L']+position['lower_leg_R']),
        "foot":mass['foot']*(position['foot_L']+position['foot_R'])
    }

    gravity_zone=1/total_mass*(part_gravity["head"]+part_gravity["neck"]+part_gravity["body"]+part_gravity["upper_arm"]+part_gravity["lower_arm"]+part_gravity["hand"]+part_gravity["upper_leg"]+part_gravity["lower_leg"]+part_gravity["foot"])
    rospy.loginfo(gravity_zone)
    return gravity_zone

def savefig(rgb_array,np_pred_keypoints):
    img=rgb_array
    remap_img=results_path+"/remap/"+str(time.time())+".png"

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
            radius=3,
            color=paintCol,
            thickness=1,
            lineType=cv2.LINE_4,
            shift=0)
        cv2.putText(img,
                text=str(round(float(keypoint[2]),3)),
                org=(int(keypoint[0])+10, int(keypoint[1])),
                fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                fontScale=0.7,
                color=paintCol,
                thickness=1,
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

def ImageCallback_ZED(rgb_data,dpt_data,info_data):
    # rospy.loginfo("####### debug ROI #######")
    now=rospy.get_time()
    rgb_array = np.frombuffer(rgb_data.data, dtype=np.uint8).reshape(rgb_data.height, rgb_data.width, -1)
    rgb_array=np.nan_to_num(rgb_array, copy=False)
    rgb_array=cv2.cvtColor(rgb_array,cv2.COLOR_BGR2RGB)

    dpt_array=CvBridge().imgmsg_to_cv2(dpt_data)
    dpt_array=np.array(dpt_array,dtype=np.float32)
    dpt_array=np.where(dpt_array>40,0,dpt_array)
    dpt_array=np.where(dpt_array<0,0,dpt_array)
    # rospy.loginfo(dpt_array)

    proj_mtx=np.array(info_data.P).reshape(3,4)
    
    # keypoint detection
    np_pred_keypoints=detect_kp(rgb_array)
    # rospy.loginfo(np_pred_keypoints)

    # 2D to 3D
    np_pred_keypoints_3D=get_position_kp(rgb_array,dpt_array,np_pred_keypoints,proj_mtx)
    
    # gravity
    gravity_zone=get_gravity_zone(np_pred_keypoints_3D)

    # save gravity
    gravity_zone.tolist().insert(0,time.time())
    gravity_history.append(gravity_zone)
    np.savetxt(csv_path,gravity_history)

    # savefig(rgb_array,np_pred_keypoints)
    
    # objects=results.pandas().xyxy[0]
    # obj_people=objects[objects['name']=='person']
    # rect_list=get_position(rgb_array,dpt_array,obj_people,proj_mtx)

    # get_velocity(rect_list,now)
    # export_csv(rect_list,now)


# topicName_rgb="/camera3/camera/color/image_raw"
# topicName_dpt="/camera3/camera/aligned_depth_to_color/image_raw"
# topicName_camInfo="/camera3/camera/aligned_depth_to_color/camera_info"
topicName_rgb="/zed/zed_node/rgb/image_rect_color"
topicName_dpt="/zed/zed_node/depth/depth_registered"
topicName_camInfo="/zed/zed_node/rgb/camera_info"

results_path="/home/hayashide/catkin_ws/src/sotsuron_experiment/images/results"



detector=Detector(model_type="KP")

# subscribe
mf=pub_sub()
# mf.registerCallback(ImageCallback_realsense)
mf.registerCallback(ImageCallback_ZED)
rospy.spin()





# sources_path="/home/hayashide/catkin_ws/src/sotsuron_experiment/images/sources"
# sources=sorted(glob(sources_path+"/*"))
# print(sources)

# results_path="/home/hayashide/catkin_ws/src/sotsuron_experiment/images/results"

# for source in sources:
#     pic_path=os.path.basename(source)
#     detectron2_img=results_path+pic_path
#     remap_img=results_path+"/remap/"+pic_path

#     detector=Detector(model_type="KP")
#     start=time.time()
#     pred_keypoints=detector.onImage(source,detectron2_img)
#     print(time.time()-start)

#     try:
#         np_pred_keypoints=pred_keypoints.to(torch.device('cpu')).detach().clone().numpy()[0]
#     except IndexError:
#         continue
#     print(np_pred_keypoints)

#     img=cv2.imread(source)

#     for i,keypoint in enumerate(np_pred_keypoints):
#         if float(keypoint[2])<0.4:
#             paintCol=(0,0,255*(float(keypoint[2])+0.4))
#             pass
#         elif float(keypoint[2])<0.7:
#             paintCol=(0,255*(float(keypoint[2])+0.7),0)
#             pass
#         else:
#             paintCol=(255*(float(keypoint[2])),0,0)
#             pass
#         cv2.circle(img,
#             center=(int(keypoint[0]), int(keypoint[1])),
#             radius=10,
#             color=paintCol,
#             thickness=3,
#             lineType=cv2.LINE_4,
#             shift=0)
#         cv2.putText(img,
#                 text=str(round(float(keypoint[2]),3)),
#                 org=(int(keypoint[0])+10, int(keypoint[1])),
#                 fontFace=cv2.FONT_HERSHEY_SIMPLEX,
#                 fontScale=0.7,
#                 color=paintCol,
#                 thickness=2,
#                 lineType=cv2.LINE_4)
#         cv2.putText(img,
#                 text=str(i),
#                 org=(int(keypoint[0])-30, int(keypoint[1])),
#                 fontFace=cv2.FONT_HERSHEY_SIMPLEX,
#                 fontScale=0.7,
#                 color=paintCol,
#                 thickness=2,
#                 lineType=cv2.LINE_4)

#     cv2.imwrite(remap_img,img)