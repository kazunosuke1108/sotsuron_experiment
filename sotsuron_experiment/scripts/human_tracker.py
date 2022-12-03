#! /usr/bin/python3
# -*- coding: utf-8 -*-

import os
import sys
import json
import time
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

# ROS preparation
rospy.init_node('human_tracker')

# yolov5 model import
model = torch.hub.load("/usr/local/lib/python3.8/dist-packages/yolov5", 'custom', path=os.environ['HOME']+'/catkin_ws/src/object_detector/config/yolov5/yolov5s.pt',source='local')

# dpt history
dpt_history=[]

# csv
csv_path=os.environ['HOME']+"/catkin_ws/src/sotsuron_experiment/scripts/monitor/results.csv"

# json
jsn_path=os.environ['HOME']+"/catkin_ws/src/sotsuron_experiment/scripts/monitor/velocity.json"

# end_flg
end_flg=False
end_semi_flg=False

# end_thre
end_thre=18

try:
    os.remove(csv_path)
    os.remove(jsn_path)
except FileNotFoundError:
    pass

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

def get_position(rgb_array,dpt_array,obj_people,proj_mtx):
    # size translation
    y_rgb2dpt=dpt_array.shape[0]/rgb_array.shape[0]
    x_rgb2dpt=dpt_array.shape[1]/rgb_array.shape[1]
    # リストの中に辞書が入っていて、その中に情報が埋め込まれてる
    """
    辞書の中身
    0. xmin_dpt
    1. ymin_dpt
    2. xmax_dpt
    3. ymax_dpt
    4. bd_center_x
    5. bd_center_y
    6. center_3d
    7. confidence
    8. dpt

    """
    rect_list=[]

    for i,row in enumerate(obj_people.itertuples()):
        xmin_dpt=row.xmin*x_rgb2dpt
        ymin_dpt=row.ymin*y_rgb2dpt
        xmax_dpt=row.xmax*x_rgb2dpt
        ymax_dpt=row.ymax*y_rgb2dpt
        confidence=row.confidence
        bd_box=np.array(dpt_array[int(ymin_dpt):int(ymax_dpt),int(xmin_dpt):int(xmax_dpt)])
        dpt=np.nanmedian(bd_box)
        bd_center_y=int((ymin_dpt+ymax_dpt)/2)
        bd_center_x=int((xmin_dpt+xmax_dpt)/2)
        center_3d=dpt*np.dot(np.linalg.pinv(proj_mtx),np.array([bd_center_x,bd_center_y,1]).T)
        one_person={
            'xmin_dpt':int(xmin_dpt),
            'ymin_dpt':int(ymin_dpt),
            'xmax_dpt':int(xmax_dpt),
            'ymax_dpt':int(ymax_dpt),
            'bd_center_x':bd_center_x,
            'bd_center_y':bd_center_y,
            'center_3d':center_3d,
            'confidence':confidence,
            'dpt':dpt
            }
        rect_list.append(one_person)
        print(one_person)
    return rect_list

def export_csv(rect_list,now):
    if len(rect_list)>0:
        center_3d=rect_list[0]['center_3d']
        if np.isnan(center_3d).any():
            rospy.loginfo("export csv: remove nan")
        else:
            center_3d=rect_list[0]['center_3d']
            export_data=center_3d.tolist()
            export_data.insert(0,now)
            dpt_history.append(export_data)
        np.savetxt(csv_path,dpt_history,delimiter=",")
        rospy.loginfo(center_3d)
    else:
        rospy.loginfo("get_velocity: No one detected")

# def get_velocity(rect_list,now):
#     if len(rect_list)>0:
#         one_person=rect_list[0]['center_3d'].tolist()
#         one_person.insert(0,now)

#         if len(dpt_history)>=2:
#             #velocity=np.sqrt((dpt_history[-1][1]-dpt_history[-2][1])**2+(dpt_history[-1][2]-dpt_history[-2][2])**2+(dpt_history[-1][3]-dpt_history[-2][3])**2)/(dpt_history[-1][0]-dpt_history[-2][0])
#             velocity=(one_person[3]-dpt_history[-1][3])/(now-dpt_history[-1][0])
#             one_person.insert(len(one_person),velocity)
#             if rect_list[0]['center_3d'].tolist()[2]!=0 and str(rect_list[0]['center_3d'][2])!="nan":
#                 rospy.loginfo(f"{velocity} m/s")
#                 dpt_history.append(one_person)
#         else:
#             one_person.insert(len(one_person),0)
#             dpt_history.append(one_person)
        
#         np.savetxt(csv_path,dpt_history,delimiter=",")
#     else:
#         rospy.loginfo("get_velocity: No one detected")

def save_vel():
    data=np.loadtxt(csv_path,delimiter=",")
    z_list=data[:,3]
    t_list=data[:,0]
    # 線形近似
    a,b=np.polyfit(t_list,z_list,1)
    vel_info={
        "z_ave":np.average(z_list[-10:]),
        "z_latest":z_list[-1],
        "z_linear_a":a,
        "z_linear_b":b,
    }
    # print(vel_list)
    # print(np.average(vel_list))
    jsn=open(jsn_path,"w")
    json.dump(vel_info,jsn)
    jsn.close()
    rospy.loginfo(f"### velocity recognition summary ###")
    rospy.loginfo(vel_info)
    rospy.loginfo(f"### velocity recognition summary end ###")
    pass
    
# def ImageCallback_realsense(rgb_data,dpt_data,info_data):
#     try:
#         # unpack arrays
#         now=time.time()
#         rgb_array = np.frombuffer(rgb_data.data, dtype=np.uint8).reshape(rgb_data.height, rgb_data.width, -1)
#         rgb_array=np.nan_to_num(rgb_array)
#         rgb_array=cv2.cvtColor(rgb_array,cv2.COLOR_BGR2RGB)
#         dpt_array = np.frombuffer(dpt_data.data, dtype=np.uint16).reshape(dpt_data.height, dpt_data.width, -1)
#         dpt_array=np.nan_to_num(dpt_array)
#         proj_mtx=np.array(info_data.P).reshape(3,4)
#         # object recognition
#         results=model(rgb_array)
#         objects=results.pandas().xyxy[0]
#         obj_people=objects[objects['name']=='person']
#         rect_list=get_position(rgb_array,dpt_array,obj_people,proj_mtx)
#         get_velocity(rect_list,now)
#         if len(dpt_history)>=100:
#             rgb_sub.unregister()
#             dpt_sub.unregister()
#             info_sub.unregister()
#             save_vel(1500)
#             rospy.on_shutdown(save_vel)


#     except Exception:
#             exc_type, exc_obj, exc_tb = sys.exc_info()
#             fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
#             pprint(exc_type, fname, exc_tb.tb_lineno)


def ImageCallback_ZED(rgb_data,dpt_data,info_data):
    global end_flg, end_semi_flg
    # try:
        # unpack arrays
    now=rospy.get_time()
    rgb_array = np.frombuffer(rgb_data.data, dtype=np.uint8).reshape(rgb_data.height, rgb_data.width, -1)
    rgb_array=np.nan_to_num(rgb_array, copy=False)
    rgb_array=cv2.cvtColor(rgb_array,cv2.COLOR_BGR2RGB)

    dpt_array=CvBridge().imgmsg_to_cv2(dpt_data)
    dpt_array=np.array(dpt_array,dtype=np.float32)
    dpt_array=np.where(dpt_array>40,0,dpt_array)
    dpt_array=np.where(dpt_array<0,0,dpt_array)

    proj_mtx=np.array(info_data.P).reshape(3,4)
    
    # object recognition
    results=model(rgb_array)
    objects=results.pandas().xyxy[0]
    obj_people=objects[objects['name']=='person']
    rect_list=get_position(rgb_array,dpt_array,obj_people,proj_mtx)

    # get_velocity(rect_list,now)
    export_csv(rect_list,now)

    if end_flg:
        save_vel()
        rgb_sub.unregister()
        dpt_sub.unregister()
        info_sub.unregister()
        rospy.on_shutdown(save_vel)
    else: 
        try: # 2回連続で基準値を下回ったら次の時点で終了
            if rect_list[0]['center_3d'][2]<end_thre:
                if end_semi_flg:
                    end_flg=True
                else:
                    end_semi_flg=True
            else:
                end_semi_flg=False
        except IndexError:
            pass



    # except Exception:
    #         exc_type, exc_obj, exc_tb = sys.exc_info()
    #         fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    #         rospy.loginfo(f"{exc_type}, {fname},{ exc_tb.tb_lineno}")



# topicName_rgb="/camera3/camera/color/image_raw"
# topicName_dpt="/camera3/camera/aligned_depth_to_color/image_raw"
# topicName_camInfo="/camera3/camera/aligned_depth_to_color/camera_info"
topicName_rgb="/zed/zed_node/rgb/image_rect_color"
topicName_dpt="/zed/zed_node/depth/depth_registered"
topicName_camInfo="/zed/zed_node/rgb/camera_info"



# subscribe
mf=pub_sub()
# mf.registerCallback(ImageCallback_realsense)
mf.registerCallback(ImageCallback_ZED)
rospy.spin()
