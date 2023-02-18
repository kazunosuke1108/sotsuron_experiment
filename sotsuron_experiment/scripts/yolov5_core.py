#! /usr/bin/python3
# -*- coding: utf-8 -*-

import os
import numpy as np
import torch
import rospy

model = torch.hub.load("/usr/local/lib/python3.8/dist-packages/yolov5", 'custom', path=os.environ['HOME']+'/catkin_ws/src/object_detector/config/yolov5/yolov5s.pt',source='local')

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
        rospy.loginfo(dpt)
    return rect_list

def get_position_yolov5(rgb_array,dpt_array,proj_mtx):
    # detect
    results=model(rgb_array)
    objects=results.pandas().xyxy[0]
    obj_people=objects[objects['name']=='person']

    # get position
    y_rgb2dpt=dpt_array.shape[0]/rgb_array.shape[0]
    x_rgb2dpt=dpt_array.shape[1]/rgb_array.shape[1]
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

        # print(proj_mtx)

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
    try:
        return rect_list[0]
    except IndexError:
        dummy={
            'xmin_dpt':np.nan,
            'ymin_dpt':np.nan,
            'xmax_dpt':np.nan,
            'ymax_dpt':np.nan,
            'bd_center_x':np.nan,
            'bd_center_y':np.nan,
            'center_3d':np.array([np.nan,np.nan,np.nan,np.nan]),
            'confidence':np.nan,
            'dpt':np.nan
            }
        return dummy