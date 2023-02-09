#! /usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import numpy as np
import matplotlib.pyplot as plt
import rospy
from sensor_msgs.msg import Image
from sensor_msgs.msg import CameraInfo
import message_filters
import cv2
from cv_bridge import CvBridge

from kalman import kalman_filter
from yolov5_core import *

rospy.init_node('human_tracker')
start_flg=False
history=[]

graph_path="/home/hayashide/catkin_ws/src/sotsuron_experiment/results/0207/graph/"+sys.argv[1]+".png"
csv_path="/home/hayashide/catkin_ws/src/sotsuron_experiment/results/0207/csv/"+sys.argv[1]+".csv"
csv_for_m_path="/home/hayashide/catkin_ws/src/ytlab_hsr/ytlab_hsr_modules/exp_data/zed.csv"

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

def velocity_processer(buffer):
    raw_velocity=buffer[:,2]-np.insert(buffer[:-1,2],0,0)
    try:
        kalman_velocity=kalman_filter(buffer[:,2],fps=30)
        rospy.loginfo(raw_velocity)
        rospy.loginfo(kalman_velocity)
        return kalman_velocity[:,1]
    except Exception:
        return raw_velocity



def plotter(history):
    # fig=plt.figure()
    # ax1 = fig.add_subplot(2, 1, 1)
    # ax2 = fig.add_subplot(2, 1, 2)
    buffer=[]
    buffer_t=[]
    for data in history:
        temp=data['center_3d'].tolist()
        buffer.append(temp)
        buffer_t.append(data['time']-history[0]['time'])
    buffer=np.array(buffer)
    buffer_t=np.array(buffer_t)
    savedata=np.column_stack([buffer_t,buffer])
    # rospy.loginfo(savedata)
    # np.savetxt(csv_path,savedata,delimiter=",")
    np.savetxt(csv_for_m_path,savedata,delimiter=",")

    pass

"""
{'xmin_dpt': 546, 'ymin_dpt': 310, 'xmax_dpt': 563, 'ymax_dpt': 366, 'bd_center_x': 555, 'bd_center_y': 338, 'center_3d': array([     -1.587,    -0.52527,      9.8838,           0]), 'confidence': 0.27612292766571045, 'dpt': 9.883846}

"""

def ImageCallback_ZED(rgb_data,dpt_data,info_data):
    # unpack
    global end_flg, end_semi_flg
    rgb_array = np.frombuffer(rgb_data.data, dtype=np.uint8).reshape(rgb_data.height, rgb_data.width, -1)
    rgb_array=np.nan_to_num(rgb_array, copy=False)
    rgb_array=cv2.cvtColor(rgb_array,cv2.COLOR_BGR2RGB)
    dpt_array=CvBridge().imgmsg_to_cv2(dpt_data)
    dpt_array=np.array(dpt_array,dtype=np.float32)
    dpt_array=np.where(dpt_array>20,0,dpt_array)
    dpt_array=np.where(dpt_array<0,0,dpt_array)
    proj_mtx=np.array(info_data.P).reshape(3,4)

    # detection
    data=get_position_yolov5(rgb_array,dpt_array,proj_mtx)
    try:
        data['time']=int(str(rgb_data.header.stamp))/1e9
    except TypeError:
        data['time']=0
        pass
    
    # history
    history.append(data)
    # plot
    plotter(history)
    rospy.loginfo(data)


topicName_rgb="/zed/zed_node/rgb/image_rect_color"
topicName_dpt="/zed/zed_node/depth/depth_registered"
topicName_camInfo="/zed/zed_node/rgb/camera_info"

mf=pub_sub()
mf.registerCallback(ImageCallback_ZED)
rospy.spin()